/*
 * Copyright (c) 2019 Nobuyuki Umetani
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#include <vector>
#include <map>
#include <deque>

#include "../py_funcs.h"

#include "delfem2/mat3.h"
#include "delfem2/mshtopoio.h"
#include "delfem2/voxel.h"
#include "delfem2/bv.h"
#include "delfem2/primitive.h"
#include "delfem2/iss.h"
#include "delfem2/mathexpeval.h"

#include "delfem2/cad2d.h"
#include "delfem2/rig_v3q.h"

#include "delfem2/../../external/tinygltf/tiny_gltf.h"
#include "delfem2/../../external/io_gltf.h"

namespace py = pybind11;

//////////////////////////////////////////////////////////////////////////////////////////


void init_polyline(py::module &m);
void init_mshtopoio(py::module &m);
void init_field(py::module &m);
void init_fem(py::module &m);
void init_sdf(py::module &m);



std::tuple<std::vector<double>,std::vector<unsigned int>> PyMeshQuad3D_VoxelGrid
(const CVoxelGrid3D& vg)
{
  std::vector<double> aXYZ;
  std::vector<unsigned int> aQuad;
  vg.GetQuad(aXYZ, aQuad);
  return std::make_tuple(aXYZ,aQuad);
}

std::tuple<std::vector<double>,std::vector<int>> PyMeshHex3D_VoxelGrid
(const CVoxelGrid3D& vg)
{
  std::vector<double> aXYZ;
  std::vector<int> aHex;
  vg.GetHex(aXYZ, aHex);
  return std::make_tuple(aXYZ,aHex);
}

std::tuple<py::array_t<double>, py::array_t<unsigned int>>
NumpyXYTri_MeshDynTri2D
(CMeshDynTri2D& dmesh)
{
  std::vector<double> aXY;
  std::vector<unsigned int> aTri;
  dmesh.Export_StlVectors(aXY,aTri);
  py::array_t<double> npXY({(int)aXY.size()/2,2}, aXY.data());
  py::array_t<unsigned int> npTri({(int)aTri.size()/3,3}, aTri.data());
  return std::make_tuple(npXY,npTri);
}

py::array_t<int> PyCad2D_GetPointsEdge
(const CCad2D& cad,
 const std::vector<int>& aIE,
 const py::array_t<double>& aXY,
 double torelance)
{
  std::vector<int> aIdP;
  cad.GetPointsEdge(aIdP,
                    aXY.data(), aXY.shape()[0],
                    aIE,torelance);
  std::set<int> setIdP(aIdP.begin(),aIdP.end());
  aIdP.assign(setIdP.begin(),setIdP.end());
  return py::array_t<int>((int)aIdP.size(), aIdP.data());
}

py::array_t<double> PyMVC
(const py::array_t<double>& XY,
 const py::array_t<double>& XY_bound)
{
  assert( AssertNumpyArray2D(XY, -1, 2) );
  assert( AssertNumpyArray2D(XY_bound, -1, 2) );
  const int np = XY.shape()[0];
  const int npb = XY_bound.shape()[0];
  py::array_t<double> aW({np,npb});
  auto buff_w = aW.request();
  for(int ip=0;ip<np;++ip){
    MeanValueCoordinate2D((double*)buff_w.ptr+ip*npb,
                          XY.at(ip,0), XY.at(ip,1),
                          XY_bound.data(), npb);
  }
  return aW;
}


py::array_t<double> PyRotMat3_Cartesian(const std::vector<double>& d)
{
  CMatrix3 m;
  m.SetRotMatrix_Cartesian(d[0], d[1], d[2]);
  py::array_t<double> npR({3,3});
  for(int i=0;i<3;++i){
    for(int j=0;j<3;++j){
      npR.mutable_at(i,j) = m.Get(i, j);
    }
  }
  return npR;
}

std::tuple<py::array_t<double>, py::array_t<unsigned int>, py::array_t<double>, py::array_t<unsigned int>>
PyGLTF_GetMeshInfo
(const CGLTF& gltf,
 int imesh, int iprimitive)
{
  std::vector<double> aXYZ0;
  std::vector<unsigned int> aTri;
  std::vector<double> aRigWeight;
  std::vector<unsigned int> aRigJoint;
  gltf.GetMeshInfo(aXYZ0,aTri,aRigWeight,aRigJoint,
                   imesh, iprimitive);
  const int np = aXYZ0.size()/3;
  assert( (int)aRigWeight.size() == np*4 );
  assert( (int)aRigJoint.size() == np*4 );
  py::array_t<double> npXYZ0({np,3}, aXYZ0.data());
  py::array_t<unsigned int> npTri({(int)aTri.size()/3,3}, aTri.data());
  py::array_t<double> npRW({np,4}, aRigWeight.data());
  py::array_t<unsigned int> npRJ({np,4}, aRigJoint.data());
  return std::make_tuple(npXYZ0,npTri,npRW,npRJ);
}

class CBoneArray{
public:
  void SetTranslation(int ib, const std::vector<double>& aT){
    assert(aT.size()==3);
    aRigBone[ib].SetTranslation(aT[0], aT[1], aT[2]);
    UpdateBoneRotTrans(aRigBone);
  }
  void SetRotationBryant(int ib, const std::vector<double>& aRB){
    assert(aRB.size()==3);
    aRigBone[ib].SetRotationBryant(aRB[0], aRB[1], aRB[2]);
    UpdateBoneRotTrans(aRigBone);
  }
public:
  std::vector<CRigBone> aRigBone;
};

CBoneArray
PyGLTF_GetBones
(const CGLTF& gltf,
 int iskin)
{
  CBoneArray BA;
  gltf.GetBone(BA.aRigBone,
               iskin);
  return BA;
}

void PyUpdateRigSkin
(py::array_t<double>& npXYZ,
 const py::array_t<double>& npXYZ0,
 const py::array_t<unsigned int>& npTri,
 const CBoneArray& BA,
 const py::array_t<double>& npRigWeight,
 const py::array_t<unsigned int>& npRigJoint)
{
  assert( AssertNumpyArray2D(npXYZ, -1, 3) );
  assert( AssertNumpyArray2D(npXYZ0, -1, 3) );
  assert( AssertNumpyArray2D(npTri, -1, 3) );
  assert( AssertNumpyArray2D(npRigWeight, -1, 4) );
  assert( AssertNumpyArray2D(npRigJoint, -1, 4) );
  assert( npXYZ.shape()[0] == npXYZ0.shape()[0] );
  assert( npXYZ.shape()[0] == npRigWeight.shape()[0] );
  assert( npXYZ.shape()[0] == npRigJoint.shape()[0] );
  double* aXYZ = (double*)(npXYZ.request().ptr);
  UpdateRigSkin(aXYZ,
                npXYZ0.data(), npXYZ0.shape()[0],
                npTri.data(), npTri.shape()[0],
                BA.aRigBone,
                npRigWeight.data(),
                npRigJoint.data());
}


PYBIND11_MODULE(c_core, m) {
  m.doc() = "pybind11 delfem2 binding";
  ///////////////////////////////////
  
  init_mshtopoio(m);
  init_polyline(m);
  init_field(m);
  init_fem(m);
  init_sdf(m);
  
  ///////////////////////////////////
  // axis arrigned boudning box
  py::class_<CBV3D_AABB>(m,"AABB3", "3D axis aligned bounding box class")
  .def(py::init<>())
  .def(py::init<const std::vector<double>&>())
  .def("__str__",            &CBV3D_AABB::str, "print x_min,x_max,y_min,y_max,z_min,z_max")
  .def("minmax_xyz",         &CBV3D_AABB::MinMaxXYZ)
  .def("set_minmax_xyz",     &CBV3D_AABB::SetMinMaxXYZ)
  .def("add_minmax_xyz",     &CBV3D_AABB::Add_AABBMinMax)
  .def("list_xyz",           &CBV3D_AABB::Point3D_Vox, "corner xyz coords in voxel point order")
  .def("diagonal_length",    &CBV3D_AABB::DiagonalLength, "diagonal length of the bounding box")
  .def("max_length",         &CBV3D_AABB::MaxLength, "diagonal length of the bounding box")
  .def("center",             &CBV3D_AABB::Center, "center position")
  .def_readwrite("isActive", &CBV3D_AABB::is_active);
  
  ///////////////////////////////////
  // voxel
  py::class_<CVoxelGrid3D>(m, "CppVoxelGrid", "voxel grid class")
  .def(py::init<>())
  .def("add",&CVoxelGrid3D::Add,"add voxel at the integer coordinate");
  
  m.def("meshquad3d_voxelgrid",&PyMeshQuad3D_VoxelGrid);
  m.def("meshhex3d_voxelgrid", &PyMeshHex3D_VoxelGrid);
  
  ///////////////////////////////////
  // cad
  py::class_<CCad2D>(m, "CppCad2D", "2D CAD class")
  .def(py::init<>())
  .def("pick",        &CCad2D::Pick)
  .def("drag_picked", &CCad2D::DragPicked)
  .def("minmax_xyz",  &CCad2D::MinMaxXYZ)
  .def("add_polygon", &CCad2D::AddPolygon)
  .def("xy_vtxctrl_face", &CCad2D::XY_VtxCtrl_Face)
  .def("ind_vtx_face", &CCad2D::Ind_Vtx_Face)
  .def("ind_edge_face",&CCad2D::Ind_Edge_Face)
  .def("ind_vtx_edge", &CCad2D::Ind_Vtx_Edge)
  .def("add_vtx_edge", &CCad2D::AddVtxEdge)
  .def("set_edge_type",&CCad2D::SetEdgeType)
  .def("edge_type",   &CCad2D::GetEdgeType)
  .def("check",       &CCad2D::Check)
  .def("nface",       &CCad2D::nFace)
  .def("nvtx",        &CCad2D::nVtx)
  .def("nedge",       &CCad2D::nEdge)
  .def_readwrite("is_draw_face", &CCad2D::is_draw_face)
  .def_readwrite("ivtx_picked",  &CCad2D::ivtx_picked)
  .def_readwrite("iedge_picked",  &CCad2D::iedge_picked)
  .def_readwrite("iface_picked",  &CCad2D::iface_picked);
  
  py::class_<CMesher_Cad2D>(m,"CppMesher_Cad2D")
  .def(py::init<>())
  .def("meshing",            &CMesher_Cad2D::Meshing)
  .def("points_on_one_edge",    &CMesher_Cad2D::IndPoint_IndEdge)
  .def("points_on_edges",    &CMesher_Cad2D::IndPoint_IndEdgeArray)
  .def("points_on_faces",    &CMesher_Cad2D::IndPoint_IndFaceArray)
  .def_readwrite("edge_length", &CMesher_Cad2D::edge_length);

  m.def("cad_getPointsEdge",
        &PyCad2D_GetPointsEdge,
        py::arg("cad"),
        py::arg("list_edge_index"),
        py::arg("np_xy"),
        py::arg("tolerance") = 0.001,
        py::return_value_policy::move);
  
  m.def("numpyXYTri_MeshDynTri2D",&NumpyXYTri_MeshDynTri2D);
  
  /*
  py::class_<CRigBone>(m,"CppRigBone")
  .def(py::init<>())
  .def("set_translation", &CRigBone::SetTranslation)
  .def("set_rotation_bryant", &CRigBone::SetRotationBryant);
   */
  
  py::class_<CGLTF>(m,"CppGLTF")
  .def(py::init<>())
  .def("read", &CGLTF::Read)
  .def("print", &CGLTF::Print);
  
  py::class_<CBoneArray>(m,"CppBoneArray")
  .def("set_translation", &CBoneArray::SetTranslation)
  .def("set_rotation_bryant", &CBoneArray::SetRotationBryant)
  .def(py::init<>());
  
  m.def("CppGLTF_GetMeshInfo", &PyGLTF_GetMeshInfo);
  m.def("CppGLTF_GetBones", &PyGLTF_GetBones);
  m.def("update_rig_skin", &PyUpdateRigSkin);
  m.def("update_bone_transform", &UpdateBoneRotTrans);

  
  ////////////////////////////////////

  py::class_<CMathExpressionEvaluator>(m,"MathExpressionEvaluator")
  .def(py::init<>())
  .def("set_expression",&CMathExpressionEvaluator::SetExp)
  .def("set_key",       &CMathExpressionEvaluator::SetKey)
  .def("eval",          &CMathExpressionEvaluator::Eval);
  
  m.def("mvc",              &PyMVC);
  m.def("rotmat3_cartesian", &PyRotMat3_Cartesian);
}


