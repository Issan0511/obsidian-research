"""step_E_yi_fit.py — Y_i の関数形 fitting

以下 4 関数形で per-arm per-kp 群回帰:
  (i)   Y = c1 · v^2 · f1(kon, zbar_kick)
  (ii)  Y = c2 · |v| · f2(kon, zbar_kick)
  (iii) Y = c3 · v^2 · g(zmax_kick)   (§3-10「着地点 z_max 高いほど上がる」)
  (iv)  Y = c4 · v^2 · sign(v · Σ_{r∈on} δ'_r) · h(...)   (§3-10 の 70% predictor)

各 form の R² を per-arm per-kp 群で比較、c_j(η) を 5 arm で log-log fit。

入力: step_D_y_per_event.npz
出力:
  session21_out/step_E_yi_functional_form.md
  session21_out/step_E_yi_fits.json
"""
import numpy as np, sys, os, json
from scipy.stats import spearmanr

OUT = '/home/kubo/project/Nakatsuka/claude/hole1_scripts/session21_out'
ETAS = {'0156': 0.000156, '02': 0.0002, '05': 0.0005, '10': 0.001, '25': 0.0025}
TAGS = list(ETAS.keys())


def r2(y_true, y_pred):
    y_true = y_true.astype(np.float64); y_pred = y_pred.astype(np.float64)
    ss_res = ((y_true - y_pred) ** 2).sum()
    ss_tot = ((y_true - y_true.mean()) ** 2).sum() + 1e-30
    return 1 - ss_res / ss_tot


def linfit_1d(x, y):
    """slope, intercept, R² of y ~ slope * x + intercept."""
    x = x.astype(np.float64); y = y.astype(np.float64)
    A = np.vstack([x, np.ones_like(x)]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    slope, intercept = float(coef[0]), float(coef[1])
    y_pred = slope * x + intercept
    return slope, intercept, r2(y, y_pred)


def linfit_no_intercept(x, y):
    """slope of y ~ slope * x (no intercept)."""
    x = x.astype(np.float64); y = y.astype(np.float64)
    denom = (x * x).sum() + 1e-30
    slope = float((x * y).sum() / denom)
    y_pred = slope * x
    return slope, r2(y, y_pred)


def fit_form(form_name, feature_fn, Y, features):
    """
    Y: (N,) target
    features: dict of arrays used by feature_fn
    Returns: dict with slope, intercept, R2
    """
    x = feature_fn(**features)
    mask = np.isfinite(x) & np.isfinite(Y)
    xm, ym = x[mask], Y[mask]
    if xm.size < 100:
        return dict(slope=float('nan'), intercept=float('nan'), R2=float('nan'), n=int(xm.size))
    slope, intercept, R2 = linfit_1d(xm, ym)
    slope_ni, R2_ni = linfit_no_intercept(xm, ym)
    return dict(slope=slope, intercept=intercept, R2=R2,
                slope_no_intercept=slope_ni, R2_no_intercept=R2_ni,
                n=int(xm.size), x_mean=float(xm.mean()), y_mean=float(ym.mean()))


def main():
    log = ['# Step E — Y_i の関数形 fitting', '']
    def L(s):
        print(s, flush=True); log.append(s)

    L('入力: step_D_y_per_event.npz')
    inp = os.path.join(OUT, 'step_D_y_per_event.npz')
    d = np.load(inp)

    all_fits = {}
    for tag in TAGS:
        eta = ETAS[tag]
        pref = f'{tag}__'
        if pref + 'Y' not in d.files:
            L(f'\n## lr{tag}: missing')
            continue
        Y = d[pref + 'Y'].ravel()
        v = d[pref + 'v'].ravel()
        v2 = d[pref + 'v2'].ravel()
        zbar_pre = d[pref + 'zbar_pre'].ravel()
        zbar_kick = d[pref + 'zbar_kick'].ravel()
        zmax_kick = d[pref + 'zmax_kick'].ravel()
        kon = d[pref + 'kon_kick'].ravel()
        sum_dprime_on = d[pref + 'sum_dprime_on'].ravel()
        sgn_pred = d[pref + 'sgn_pred'].astype(np.float32).ravel()

        L(f'\n## lr{tag} (η={eta:g})  n={Y.size}')

        fits_this = {}
        for kp_label, mask in [
            ('kp0', kon == 0),
            ('kp1', kon == 1),
            ('kp2', kon == 2),
            ('kp3-5', (kon >= 3) & (kon <= 5)),
            ('kp6+', kon >= 6),
            ('all', np.ones_like(kon, dtype=bool)),
        ]:
            Ym = Y[mask]
            vm = v[mask]; v2m = v2[mask]; zpm = zbar_pre[mask]; zkm = zbar_kick[mask]
            zmxm = zmax_kick[mask]; sdo = sum_dprime_on[mask]; spr = sgn_pred[mask]
            n = int(mask.sum())
            if n < 200:
                continue
            # form (i): Y ~ c1 · v²
            f_i = fit_form('v2', lambda **k: k['v2'], Ym, dict(v2=v2m))
            # form (ii): Y ~ c2 · |v|
            f_ii = fit_form('absv', lambda **k: np.abs(k['v']), Ym, dict(v=vm))
            # form (iii): Y ~ c3 · v² · z_max_kick
            f_iii = fit_form('v2_zmax', lambda **k: k['v2'] * k['zmax'], Ym, dict(v2=v2m, zmax=zmxm))
            # form (iv): Y ~ c4 · v² · sgn_pred
            f_iv = fit_form('v2_sgn', lambda **k: k['v2'] * k['sgn'], Ym, dict(v2=v2m, sgn=spr))
            # form (v): Y ~ c5 · v · sum_dprime_on (the sgn predictor's raw form)
            f_v = fit_form('v_sumdprime_on', lambda **k: k['v'] * k['sdo'], Ym, dict(v=vm, sdo=sdo))
            # form (vi): Y ~ c6 · v² · zbar_kick
            f_vi = fit_form('v2_zbarkick', lambda **k: k['v2'] * k['zk'], Ym, dict(v2=v2m, zk=zkm))
            # form (vii): sgn predictor test — Spearman between Y and sgn_pred
            try:
                res = spearmanr(Ym, spr)
                rho = float(getattr(res, 'statistic', getattr(res, 'correlation', float('nan'))))
            except Exception:
                rho = float('nan')

            fits_this[kp_label] = dict(
                n=n, Y_mean=float(Ym.mean()), Y_std=float(Ym.std()),
                v2=f_i, absv=f_ii, v2_zmax=f_iii, v2_sgn=f_iv,
                v_sumdprime_on=f_v, v2_zbarkick=f_vi,
                spearman_Y_sgnpred=float(rho))

            L(f'### {kp_label}  n={n}  Y_mean={Ym.mean():+.4f}  Y_std={Ym.std():.4f}')
            for name, f in [('(i)  v²', f_i), ('(ii) |v|', f_ii),
                            ('(iii) v²·z_max_kick', f_iii),
                            ('(iv) v²·sgn(v·Σδ\'_on)', f_iv),
                            ('(v) v·Σδ\'_on', f_v),
                            ('(vi) v²·z̄_kick', f_vi)]:
                L(f'  {name:30s}  slope={f["slope"]:+.4f}  R²={f["R2"]:+.4f}')
            L(f'  Spearman(Y, sgn_pred)={rho:+.4f}')

        all_fits[tag] = dict(eta=eta, fits=fits_this)

    # log-log fit of c(η) for each form
    etas_log = np.array([np.log(ETAS[t]) for t in TAGS])
    for form_key in ['v2', 'v_sumdprime_on', 'v2_zmax', 'v2_sgn']:
        L(f'\n## η 依存 (log-log fit of |slope|)  — form ({form_key})')
        for kp_label in ['kp1', 'kp2', 'kp3-5', 'kp6+']:
            slopes = []
            R2s = []
            for t in TAGS:
                f = all_fits.get(t, {}).get('fits', {}).get(kp_label, {}).get(form_key, {})
                slopes.append(f.get('slope', float('nan')))
                R2s.append(f.get('R2', float('nan')))
            slopes = np.array(slopes, dtype=np.float64)
            R2s = np.array(R2s, dtype=np.float64)
            valid = np.isfinite(slopes) & (slopes != 0)
            if valid.sum() >= 3:
                log_abs = np.log(np.abs(slopes[valid]))
                A = np.vstack([etas_log[valid], np.ones(valid.sum())]).T
                coef, *_ = np.linalg.lstsq(A, log_abs, rcond=None)
                mean_R2 = np.nanmean(R2s)
                L(f'  {kp_label}: slope({form_key}) [values = {slopes.tolist()}], mean R²={mean_R2:.3f}')
                L(f'    → |slope| ∝ η^{coef[0]:.2f}  C = exp({coef[1]:+.2f}) = {np.exp(coef[1]):.3e}')

    with open(os.path.join(OUT, 'step_E_yi_fits.json'), 'w') as f:
        json.dump(all_fits, f, indent=2, default=float)

    with open(os.path.join(OUT, 'step_E_yi_functional_form.md'), 'w') as f:
        f.write('\n'.join(log))
    L(f'\nsaved step_E_yi_functional_form.md and step_E_yi_fits.json')


if __name__ == '__main__':
    main()
