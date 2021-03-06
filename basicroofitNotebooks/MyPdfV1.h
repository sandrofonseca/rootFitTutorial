/*****************************************************************************
 * Project: RooFit                                                           *
 *                                                                           *
  * This code was autogenerated by RooClassFactory                            * 
 *****************************************************************************/

#ifndef MYPDFV1
#define MYPDFV1

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooCategoryProxy.h"
#include "RooAbsReal.h"
#include "RooAbsCategory.h"
 
class MyPdfV1 : public RooAbsPdf {
public:
  MyPdfV1() {} ; 
  MyPdfV1(const char *name, const char *title,
	      RooAbsReal& _x,
	      RooAbsReal& _A,
	      RooAbsReal& _B);
  MyPdfV1(const MyPdfV1& other, const char* name=0) ;
  virtual TObject* clone(const char* newname) const { return new MyPdfV1(*this,newname); }
  inline virtual ~MyPdfV1() { }

protected:

  RooRealProxy x ;
  RooRealProxy A ;
  RooRealProxy B ;
  
  Double_t evaluate() const ;

private:

  ClassDef(MyPdfV1,1) // Your description goes here...
};
 
#endif
