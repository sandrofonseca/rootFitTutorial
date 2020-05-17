#####################################
#
# 'MULTIDIMENSIONAL MODELS' ROOT.RooFit tutorial macro #306
#
# Complete example with use of conditional p.d.f. with per-event errors
#
#
#
# 07/2008 - Wouter Verkerke
#
# /


import ROOT


def rf306_condpereventerrors():
    # B - p h y s i c s   p d f   w i t h   p e r - e v e n t  G a u s s i a n   r e s o l u t i o n
    # ----------------------------------------------------------------------------------------------

    # Observables
    dt = ROOT.RooRealVar("dt", "dt", -10, 10)
    dterr = ROOT.RooRealVar("dterr", "per-event error on dt", 0.01, 10)

    # Build a gaussian resolution model scaled by the per-error =
    # gauss(dt,bias,sigma*dterr)
    bias = ROOT.RooRealVar("bias", "bias", 0, -10, 10)
    sigma = ROOT.RooRealVar(
        "sigma", "per-event error scale factor", 1, 0.1, 10)
    gm = ROOT.RooGaussModel(
        "gm1", "gauss model scaled bt per-event error", dt, bias, sigma, dterr)

    # Construct decay(dt) (x) gauss1(dt|dterr)
    tau = ROOT.RooRealVar("tau", "tau", 1.548)
    decay_gm = ROOT.RooDecay("decay_gm", "decay", dt,
                             tau, gm, ROOT.RooDecay.DoubleSided)

    # C o n s t r u c t   f a k e   ' e x t e r n a l '   d a t a    w i t h   p e r - e v e n t   e r r o r
    # ------------------------------------------------------------------------------------------------------

    # Use landau p.d.f to get somewhat realistic distribution with long tail
    pdfDtErr = ROOT.RooLandau("pdfDtErr", "pdfDtErr", dterr, ROOT.RooFit.RooConst(
        1), ROOT.RooFit.RooConst(0.25))
    expDataDterr = pdfDtErr.generate(ROOT.RooArgSet(dterr), 10000)

    # S a m p l e   d a t a   f r o m   c o n d i t i o n a l   d e c a y _ g m ( d t | d t e r r )
    # ---------------------------------------------------------------------------------------------

    # Specify external dataset with dterr values to use decay_dm as
    # conditional p.d.f.
    data = decay_gm.generate(ROOT.RooArgSet(
        dt), ROOT.RooFit.ProtoData(expDataDterr))

    # F i t   c o n d i t i o n a l   d e c a y _ d m ( d t | d t e r r )
    # ---------------------------------------------------------------------

    # Specify dterr as conditional observable
    decay_gm.fitTo(data, ROOT.RooFit.ConditionalObservables(
        ROOT.RooArgSet(dterr)))

    # P l o t   c o n d i t i o n a l   d e c a y _ d m ( d t | d t e r r )
    # ---------------------------------------------------------------------

    # Make two-dimensional plot of conditional p.d.f in (dt,dterr)
    hh_decay = decay_gm.createHistogram("hh_decay", dt, ROOT.RooFit.Binning(
        50), ROOT.RooFit.YVar(dterr, ROOT.RooFit.Binning(50)))
    hh_decay.SetLineColor(ROOT.kBlue)

    # Plot decay_gm(dt|dterr) at various values of dterr
    frame = dt.frame(ROOT.RooFit.Title(
        "Slices of decay(dt|dterr) at various dterr"))
    for ibin in range(0, 100, 20):
        dterr.setBin(ibin)
        decay_gm.plotOn(frame, ROOT.RooFit.Normalization(5.))

    # Make projection of data an dt
    frame2 = dt.frame(ROOT.RooFit.Title("Projection of decay(dt|dterr) on dt"))
    data.plotOn(frame2)

    # Make projection of decay(dt|dterr) on dt.
    #
    # Instead of integrating out dterr, a weighted average of curves
    # at values dterr_i as given in the external dataset.
    # (The kTRUE argument bins the data before projection to speed up the process)
    decay_gm.plotOn(frame2, ROOT.RooFit.ProjWData(expDataDterr, ROOT.kTRUE))

    # Draw all frames on canvas
    c = ROOT.TCanvas("rf306_condpereventerrors",
                     "rf306_condperventerrors", 1200, 400)
    c.Divide(3)
    c.cd(1)
    ROOT.gPad.SetLeftMargin(0.20)
    hh_decay.GetZaxis().SetTitleOffset(2.5)
    hh_decay.Draw("surf")
    c.cd(2)
    ROOT.gPad.SetLeftMargin(0.15)
    frame.GetYaxis().SetTitleOffset(1.6)
    frame.Draw()
    c.cd(3)
    ROOT.gPad.SetLeftMargin(0.15)
    frame2.GetYaxis().SetTitleOffset(1.6)
    frame2.Draw()

    c.SaveAs("rf306_condpereventerrors.png")


if __name__ == "__main__":
    rf306_condpereventerrors()
