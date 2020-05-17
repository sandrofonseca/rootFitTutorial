/***************************************************************************** 
 * Project: RooFit                                                           * 
 *                                                                           * 
 * This code was autogenerated by RooClassFactory                            * 
 *****************************************************************************/ 

// Your description goes here... 

#include "Riostream.h" 

#include "MyPdfV2.h" 
#include "RooAbsReal.h" 
#include "RooAbsCategory.h" 
#include <math.h> 
#include "TMath.h" 

ClassImp(MyPdfV2); 

 MyPdfV2::MyPdfV2(const char *name, const char *title, 
                        RooAbsReal& _x,
                        RooAbsReal& _A,
                        RooAbsReal& _B) :
   RooAbsPdf(name,title), 
   x("x","x",this,_x),
   A("A","A",this,_A),
   B("B","B",this,_B)
 { 
 } 


 MyPdfV2::MyPdfV2(const MyPdfV2& other, const char* name) :  
   RooAbsPdf(other,name), 
   x("x",this,other.x),
   A("A",this,other.A),
   B("B",this,other.B)
 { 
 } 



 Double_t MyPdfV2::evaluate() const 
 { 
   // ENTER EXPRESSION IN TERMS OF VARIABLE ARGUMENTS HERE 
   return A*fabs(x)+pow(x-B,2) ; 
 } 



