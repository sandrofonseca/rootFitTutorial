# /
#
# 'ADDITION AND CONVOLUTION' ROOT.RooFit tutorial macro #210
#
# Convolution in cyclical angular observables theta, and
# construction of p.d.f in terms of trasnformed angular
# coordinates, e.g. cos(theta), the convolution
# is performed in theta rather than cos(theta)
#
# (require ROOT to be compiled with --enable-fftw3)
#
# pdf(theta)    = ROOT.T(theta)          (x) gauss(theta)
# pdf(cosTheta) = ROOT.T(acos(cosTheta)) (x) gauss(acos(cosTheta))
#
#
# 04/2009 - Wouter Verkerke
#
# /


import ROOT


def rf210_angularconv():
    # S e t u p   c o m p o n e n t   p d f s
    # ---------------------------------------

    # Define angle psi
    psi = ROOT.RooRealVar("psi", "psi", 0, 3.14159268)

    # Define physics p.d.f ROOT.T(psi)
    Tpsi = ROOT.RooGenericPdf("Tpsi", "1+sin(2*@0)", ROOT.RooArgList(psi))

    # Define resolution R(psi)
    gbias = ROOT.RooRealVar("gbias", "gbias", 0.2, 0., 1)
    greso = ROOT.RooRealVar("greso", "greso", 0.3, 0.1, 1.0)
    Rpsi = ROOT.RooGaussian("Rpsi", "Rpsi", psi, gbias, greso)

    # Define cos(psi) and function psif that calculates psi from cos(psi)
    cpsi = ROOT.RooRealVar("cpsi", "cos(psi)", -1, 1)
    psif = ROOT.RooFormulaVar("psif", "acos(cpsi)", ROOT.RooArgList(cpsi))

    # Define physics p.d.f. also as function of cos(psi): ROOT.T(psif(cpsi)) =
    # ROOT.T(cpsi)
    Tcpsi = ROOT.RooGenericPdf("T", "1+sin(2*@0)", ROOT.RooArgList(psif))

    # C o n s t r u c t   c o n v o l u t i o n   p d f  i n   p s i
    # --------------------------------------------------------------

    # Define convoluted p.d.f. as function of psi: M=[T(x)R](psi) = M(psi)
    Mpsi = ROOT.RooFFTConvPdf("Mf", "Mf", psi, Tpsi, Rpsi)

    # Set the buffer fraction to zero to obtain a ROOT.True cyclical
    # convolution
    Mpsi.setBufferFraction(0)

    # S a m p l e , i t   a n d   p l o t   c o n v o l u t e d   p d f  ( p s i )
    # --------------------------------------------------------------------------------

    # Generate some events in observable psi
    data_psi = Mpsi.generate(ROOT.RooArgSet(psi), 10000)

    # Fit convoluted model as function of angle psi
    Mpsi.fitTo(data_psi)

    # Plot cos(psi) frame with Mf(cpsi)
    frame1 = psi.frame(ROOT.RooFit.Title("Cyclical convolution in angle psi"))
    data_psi.plotOn(frame1)
    Mpsi.plotOn(frame1)

    # Overlay comparison to unsmeared physics p.d.f ROOT.T(psi)
    Tpsi.plotOn(frame1, ROOT.RooFit.LineColor(ROOT.kRed))

    # C o n s t r u c t   c o n v o l u t i o n   p d f   i n   c o s ( p s i )
    # --------------------------------------------------------------------------

    # Define convoluted p.d.f. as function of cos(psi): M=[T(x)R](psif cpsi)) = M(cpsi:
    #
    # Need to give both observable psi here (for definition of convolution)
    # and function psif here (for definition of observables, in cpsi)
    Mcpsi = ROOT.RooFFTConvPdf("Mf", "Mf", psif, psi, Tpsi, Rpsi)

    # Set the buffer fraction to zero to obtain a ROOT.True cyclical
    # convolution
    Mcpsi.setBufferFraction(0)

    # S a m p l e , i t   a n d   p l o t   c o n v o l u t e d   p d f  ( c o s p s i )
    # --------------------------------------------------------------------------------

    # Generate some events
    data_cpsi = Mcpsi.generate(ROOT.RooArgSet(cpsi), 10000)

    # set psi constant to exclude to be a parameter of the fit
    psi.setConstant(True)

    # Fit convoluted model as function of cos(psi)
    Mcpsi.fitTo(data_cpsi)

    # Plot cos(psi) frame with Mf(cpsi)
    frame2 = cpsi.frame(ROOT.RooFit.Title(
        "Same convolution in psi, in cos(psi)"))
    data_cpsi.plotOn(frame2)
    Mcpsi.plotOn(frame2)

    # Overlay comparison to unsmeared physics p.d.f ROOT.Tf(cpsi)
    Tcpsi.plotOn(frame2, ROOT.RooFit.LineColor(ROOT.kRed))

    # Draw frame on canvas
    c = ROOT.TCanvas("rf210_angularconv", "rf210_angularconv", 800, 400)
    c.Divide(2)
    c.cd(1)
    ROOT.gPad.SetLeftMargin(0.15)
    frame1.GetYaxis().SetTitleOffset(1.4)
    frame1.Draw()
    c.cd(2)
    ROOT.gPad.SetLeftMargin(0.15)
    frame2.GetYaxis().SetTitleOffset(1.4)
    frame2.Draw()

    c.SaveAs("rf210_angularconv.png")


if __name__ == "__main__":
    rf210_angularconv()
