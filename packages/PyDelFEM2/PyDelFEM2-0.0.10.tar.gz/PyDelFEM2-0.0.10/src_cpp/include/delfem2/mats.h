/*
 * Copyright (c) 2019 Nobuyuki Umetani
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

#ifndef MATRIX_SPARSE_H
#define MATRIX_SPARSE_H

#include <vector>
#include <cassert>

template <typename T>
class CMatrixSparse
{
public:
  CMatrixSparse(): nblk_col(0), nblk_row(0), len_col(0), len_row(0) {}
  virtual ~CMatrixSparse(){
    colInd.clear();
    rowPtr.clear();
    valCrs.clear();
    valDia.clear();
  }  
  void Initialize(int nblk, int len, bool is_dia){
    this->nblk_col = nblk;
    this->len_col = len;
    this->nblk_row = nblk;
    this->len_row = len;
    colInd.assign(nblk+1,0);
    rowPtr.clear();
    valCrs.clear();
    if( is_dia ){ valDia.assign(nblk*len*len,0.0); }
    else{         valDia.clear(); }
  }
  void operator = (const CMatrixSparse& m){
    this->nblk_col = m.nblk_col;
    this->len_col  = m.len_col;
    this->nblk_row = m.nblk_row;
    this->len_row  = m.len_row;
    colInd = m.colInd;
    rowPtr = m.rowPtr;
    valCrs = m.valCrs;
    valDia = m.valDia; // copy value
  }
  
  void SetPattern(const int* colind, unsigned int ncolind,
                  const int* rowptr, unsigned int nrowptr){
    assert( rowPtr.empty() );
    assert( ncolind == nblk_col+1 );
    for(unsigned int iblk=0;iblk<nblk_col+1;iblk++){ colInd[iblk] = colind[iblk]; }
    const unsigned int ncrs = colind[nblk_col];
    assert( ncrs == nrowptr );
    rowPtr.resize(ncrs);
    for(unsigned int icrs=0;icrs<ncrs;icrs++){ rowPtr[icrs] = rowptr[icrs]; }
    valCrs.resize(ncrs*len_col*len_row);
  }
  bool SetZero(){
    if( valDia.size() != 0 ){
      assert( len_col == len_row );
      assert( nblk_col == nblk_row );
      const unsigned int n = valDia.size();
      assert( n == len_col*len_col*nblk_col );
      for(unsigned int i=0;i<n;++i){ valDia[i] = 0; }
    }
    {
      const unsigned int n = valCrs.size();
      assert( n == len_col*len_row*rowPtr.size() );
      for(unsigned int i=0;i<n;i++){ valCrs[i] = 0.0; }
    }
    return true;
  }
	bool Mearge(unsigned int nblkel_col, const unsigned int* blkel_col,
              unsigned int nblkel_row, const unsigned int* blkel_row,
              unsigned int blksize, const T* emat,
              std::vector<int>& m_marge_tmp_buffer);
  // Calc Matrix Vector Product
  // {y} = alpha * [A]{x} + beta * {y}  
	void MatVec(T alpha, const std::vector<T>& x, T beta,
              std::vector<T>& y) const;
  void SetBoundaryCondition(const int* pBCFlag, unsigned int nP, unsigned int ndimVal);
  void AddDia(T eps){
    assert( this->nblk_row == this->nblk_col );
    assert( this->len_row == this->len_col );
    const int blksize = len_col*len_row;
    const int nlen = this->len_col;
    if( valDia.empty() ){ return; }
    for(unsigned int ino=0;ino<nblk_col;++ino){
      for(int ilen=0;ilen<nlen;++ilen){
        valDia[ino*blksize+ilen*nlen+ilen] += eps;
      }
    }
  }
public:
	unsigned int nblk_col;
  unsigned int nblk_row;
  unsigned int len_col;
  unsigned int len_row;
  std::vector<unsigned int> colInd;
  std::vector<unsigned int> rowPtr;
  std::vector<T> valCrs;
  std::vector<T> valDia;
};


template<typename T>
void CMatrixSparse<T>::MatVec
(T alpha,
 const std::vector<T>& x,
 T beta,
 std::vector<T>& y) const
{
  const int blksize = len_col*len_col;
  const T* vcrs  = valCrs.data();
  const T* vdia = valDia.data();
  const unsigned int* colind = colInd.data();
  const unsigned int* rowptr = rowPtr.data();
  ////////////////
  for(unsigned int iblk=0;iblk<nblk_col;iblk++){
    for(unsigned int idof=0;idof<len_col;idof++){ y[iblk*len_col+idof] *= beta; }
    const unsigned int colind0 = colind[iblk];
    const unsigned int colind1 = colind[iblk+1];
    for(unsigned int icrs=colind0;icrs<colind1;icrs++){
      assert( icrs < rowPtr.size() );
      const unsigned int jblk0 = rowptr[icrs];
      assert( jblk0 < nblk_row );
      for(unsigned int idof=0;idof<len_col;idof++){
        for(unsigned int jdof=0;jdof<len_row;jdof++){
          y[iblk*len_col+idof] += alpha * vcrs[icrs*blksize+idof*len_col+jdof] * x[jblk0*len_row+jdof];
        }
      }
    }
    for(unsigned int idof=0;idof<len_col;idof++){
      for(unsigned int jdof=0;jdof<len_row;jdof++){
        y[iblk*len_col+idof] += alpha * vdia[iblk*blksize+idof*len_col+jdof] * x[iblk*len_row+jdof];
      }
    }
  }
}

template<typename T>
void CMatrixSparse<T>::SetBoundaryCondition
(const int* bc_flag, unsigned int np, unsigned int ndimval)
{
  assert( !this->valDia.empty() );
  assert( this->nblk_row == this->nblk_col );
  assert( this->len_row == this->len_col );
  assert( np == nblk_col );
  assert( ndimval == len_col );
  ////
  const int blksize = len_col*len_row;
  for(unsigned int iblk=0;iblk<nblk_col;iblk++){ // set diagonal
    for(unsigned int ilen=0;ilen<len_col;ilen++){
      if( bc_flag[iblk*len_col+ilen] == 0 ) continue;
      for(unsigned int jlen=0;jlen<len_row;jlen++){
        valDia[iblk*blksize+ilen*len_col+jlen] = 0.0;
        valDia[iblk*blksize+jlen*len_col+ilen] = 0.0;
      }
      valDia[iblk*blksize+ilen*len_col+ilen] = 1.0;
    }
  }
  /////
  for(unsigned int iblk=0;iblk<nblk_col;iblk++){ // set row
    for(unsigned int icrs=colInd[iblk];icrs<colInd[iblk+1];icrs++){
      for(unsigned int ilen=0;ilen<len_col;ilen++){
        if( bc_flag[iblk*len_col+ilen] == 0 ) continue;
        for(unsigned int jlen=0;jlen<len_row;jlen++){
          valCrs[icrs*blksize+ilen*len_col+jlen] = 0.0;
        }
      }
    }
  }
  /////
  for(unsigned int icrs=0;icrs<rowPtr.size();icrs++){ // set column
    const int jblk1 = rowPtr[icrs];
    for(unsigned int jlen=0;jlen<len_row;jlen++){
      if( bc_flag[jblk1*len_row+jlen] == 0 ) continue;
      for(unsigned int ilen=0;ilen<len_col;ilen++){
        valCrs[icrs*blksize+ilen*len_col+jlen] = 0.0;
      }
    }
  }
}

template <typename T>
bool CMatrixSparse<T>::Mearge
(unsigned int nblkel_col, const unsigned int* blkel_col,
 unsigned int nblkel_row, const unsigned int* blkel_row,
 unsigned int blksize, const T* emat,
 std::vector<int>& marge_buffer)
{
  assert( !valCrs.empty() );
  assert( !valDia.empty() );
  assert( blksize == len_col*len_row );
  marge_buffer.resize(nblk_row);
  const unsigned int* colind = colInd.data();
  const unsigned int* rowptr = rowPtr.data();
  T* vcrs = valCrs.data();
  T* vdia = valDia.data();
  for(unsigned int iblkel=0;iblkel<nblkel_col;iblkel++){
    const unsigned int iblk1 = blkel_col[iblkel];
    assert( iblk1 < nblk_col );
    for(unsigned int jpsup=colind[iblk1];jpsup<colind[iblk1+1];jpsup++){
      assert( jpsup < rowPtr.size() );
      const int jblk1 = rowptr[jpsup];
      marge_buffer[jblk1] = jpsup;
    }
    for(unsigned int jblkel=0;jblkel<nblkel_row;jblkel++){
      const unsigned int jblk1 = blkel_row[jblkel];
      assert( jblk1 < nblk_row );
      if( iblk1 == jblk1 ){  // Marge Diagonal
        const T* pval_in = &emat[(iblkel*nblkel_row+iblkel)*blksize];
        T* pval_out = &vdia[iblk1*blksize];
        for(unsigned int i=0;i<blksize;i++){ pval_out[i] += pval_in[i]; }
      }
      else{  // Marge Non-Diagonal
        if( marge_buffer[jblk1] == -1 ) continue;
        assert( marge_buffer[jblk1] >= 0 && marge_buffer[jblk1] < (int)rowPtr.size() );
        const int jpsup1 = marge_buffer[jblk1];
        assert( rowPtr[jpsup1] == jblk1 );
        const T* pval_in = &emat[(iblkel*nblkel_row+jblkel)*blksize];
        T* pval_out = &vcrs[jpsup1*blksize];
        for(unsigned int i=0;i<blksize;i++){ pval_out[i] += pval_in[i]; }
      }
    }
    for(unsigned int jpsup=colind[iblk1];jpsup<colind[iblk1+1];jpsup++){
      assert( jpsup < rowPtr.size() );
      const int jblk1 = rowptr[jpsup];
      marge_buffer[jblk1] = -1;
    }
  }
  return true;
}


//////////////////////////////////////////////////////////////////////////////////////////////////////////////////


double CheckSymmetry(const CMatrixSparse<double>& mat);
void SetMasterSlave(CMatrixSparse<double>& mat, const int* aMSFlag);
void ScaleLeftRight(CMatrixSparse<double>& mat, const double* scale);


double Dot(const std::vector<double>& r_vec,
           const std::vector<double>& u_vec);
double DotX(const double* r_vec,
            const double* u_vec,
            int ndof);

void AXPY(double a,
          const std::vector<double>& x,
          std::vector<double>& y);
void AXPY(double a,
          const double* x,
          double* y,
          int n);

void XPlusAY(std::vector<double>& X,
             const int nDoF,
             const std::vector<int>& aBCFlag,
             double alpha,
             const std::vector<double>& Y);

void XPlusAYBZ(std::vector<double>& X,
               const int nDoF,
               const std::vector<int>& aBCFlag,
               double alpha,
               const std::vector<double>& Y,
               double beta,
               const std::vector<double>& Z);

void XPlusAYBZCW(std::vector<double>& X,
                 const int nDoF,
                 const std::vector<int>& aBCFlag,
                 double alpha,
                 const std::vector<double>& Y,
                 double beta,
                 const std::vector<double>& Z,
                 double gamma,
                 const std::vector<double>& W);

// set boundary condition
void setRHS_Zero(std::vector<double>& vec_b,
                 const std::vector<int>& aBCFlag,
                 int iflag_nonzero);

void setRHS_MasterSlave(double* vec_b,
                        int nDoF,
                        const int* aMSFlag);


void Solve_CG(double& conv_ratio,
              int& iteration,
              const CMatrixSparse<double>& mat,
              std::vector<double>& r_vec,
              std::vector<double>& u_vec);

bool Solve_BiCGSTAB(double& conv_ratio,
                    int& num_iter,
                    const CMatrixSparse<double>& mat,
                    std::vector<double>& r_vec,
                    std::vector<double>& x_vec);


#endif // MATDIA_CRS_H
