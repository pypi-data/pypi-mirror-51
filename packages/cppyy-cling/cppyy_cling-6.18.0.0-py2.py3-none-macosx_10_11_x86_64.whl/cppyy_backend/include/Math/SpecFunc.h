// @(#)root/mathcore:$Id$
// Authors: L. Moneta, A. Zsenei   08/2005

 /**********************************************************************
  *                                                                    *
  * Copyright (c) 2004 ROOT Foundation,  CERN/PH-SFT                   *
  *                                                                    *
  *                                                                    *
  **********************************************************************/

/**
    Header file declaring the special functions present in both
    MathCore and  optionally MathMore.
    The MathMore ones are included only if ROOT has been built with MathMore.
*/



#ifndef ROOT_Math_SpecFunc
#define ROOT_Math_SpecFunc


#include "RConfigure.h"



#include "Math/SpecFuncMathCore.h"

#ifdef R__HAS_MATHMORE
// in case Mathmore exists include their GSL based special functions

#include "Math/SpecFuncMathMore.h"

#endif

#endif  // ROOT_Math_SpecFunc
