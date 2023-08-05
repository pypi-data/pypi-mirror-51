// @(#)root/base:$Id$
// Author: Matevz Tadel   16/08/2006

/*************************************************************************
 * Copyright (C) 1995-2006, Rene Brun and Fons Rademakers.               *
 * All rights reserved.                                                  *
 *                                                                       *
 * For the licensing terms see $ROOTSYS/LICENSE.                         *
 * For the list of contributors see $ROOTSYS/README/CREDITS.             *
 *************************************************************************/

#ifndef ROOT_TObjectSpy
#define ROOT_TObjectSpy

//////////////////////////////////////////////////////////////////////////
//                                                                      //
// TObjectSpy, TObjectRefSpy                                            //
//                                                                      //
// Monitors objects for deletion and reflects the deletion by reverting //
// the internal pointer to zero. When this pointer is zero we know the  //
// object has been deleted. This avoids the unsafe TestBit(kNotDeleted) //
// hack. The spied object must have the kMustCleanup bit set otherwise  //
// you will get an error.                                               //
//                                                                      //
//////////////////////////////////////////////////////////////////////////

#include "TObject.h"


class TObjectSpy : public TObject {

private:
   TObjectSpy(const TObjectSpy& s); // Not implemented. : TObject(), fObj(s.fObj), fFixMustCleanupBit(s.fFixMustCleanupBit) { }
   TObjectSpy& operator=(const TObjectSpy& s); // Not implemented. { fObj = s.fObj; fFixMustCleanupBit = s.fFixMustCleanupBit; return *this; }

protected:
   TObject  *fObj;                 // object being spied
   Bool_t    fResetMustCleanupBit; // flag saying that kMustCleanup needs to be reset in dtor

public:
   TObjectSpy(TObject *obj = 0, Bool_t fixMustCleanupBit=kTRUE);
   virtual ~TObjectSpy();

   virtual void  RecursiveRemove(TObject *obj);
   TObject      *GetObject() const { return fObj; }
   void          SetObject(TObject *obj, Bool_t fixMustCleanupBit=kTRUE);

   ClassDef(TObjectSpy, 0);  // Spy object pointer for deletion
};


class TObjectRefSpy : public TObject {

private:
   TObjectRefSpy(const TObjectRefSpy& s); // Not implemented.  : TObject(), fObj(s.fObj), fFixMustCleanupBit(s.fFixMustCleanupBit) { }
   TObjectRefSpy& operator=(const TObjectRefSpy& s);  // Not implemented. { fObj = s.fObj; fFixMustCleanupBit = s.fFixMustCleanupBit; return *this; }

protected:
   TObject  *&fObj;                // object being spied
   Bool_t    fResetMustCleanupBit; // flag saying that kMustCleanup needs to be reset in dtor

public:
   TObjectRefSpy(TObject *&obj, Bool_t fixMustCleanupBit=kTRUE);
   virtual ~TObjectRefSpy();

   virtual void  RecursiveRemove(TObject *obj);
   TObject      *GetObject() const { return fObj; }

   ClassDef(TObjectRefSpy, 0);  // Spy object reference for deletion
};

#endif
