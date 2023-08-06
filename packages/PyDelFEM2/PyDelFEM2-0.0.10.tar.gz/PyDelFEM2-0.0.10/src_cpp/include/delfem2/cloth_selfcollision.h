//
//  self_collision_cloth.h
//
//  Created by Nobuyuki Umetani on 10/28/12.
//  Copyright (c) 2012 Nobuyuki Umetani. All rights reserved.
//

#ifndef contact_self_collision_cloth_h
#define contact_self_collision_cloth_h

#include <vector>

#include "bv.h"
#include "bvh.h"

// 衝突が解消された中間速度を返す
void GetIntermidiateVelocityContactResolved
(std::vector<double>& aUVWm,
 bool& is_impulse_applied,
 ////
 double dt,
 double contact_clearance,
 double mass_point,
 double cloth_contact_stiffness,
 const std::vector<double>& aXYZ,
 const std::vector<unsigned int>& aTri,
// const CJaggedArray& aEdge,
 const std::vector<int>& psup_ind,
 const std::vector<int>& psup,
 int iroot_bvh,
 const std::vector<CNodeBVH>& aNodeBVH,
 std::vector<CBV3D_AABB>& aBB);
    
#endif
