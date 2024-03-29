import astro_helpers
import numpy
import numpy.random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot
import sklearn.feature_selection
import sklearn.linear_model
import sklearn.ensemble

matplotlib.pyplot.rcParams.update({'figure.figsize':[4,2], 'figure.dpi': 300, 'font.family': 'Times New Roman', 'font.size': 10, 'text.usetex': True, 'figure.autolayout': True})

nbrs = [2,3,4,5,6,7,8,11,12,13]

gdat = numpy.genfromtxt('../../Data/GSWLC2_LOCAL/GSWLC-X2.1_CLEAN3_id_z_fnugrizbvjhk.csv', delimiter = ',')[:,nbrs] # feature data
glst = numpy.genfromtxt('../../Data/GSWLC2_LOCAL/g3_nbrs_nz_dkbk7.csv', delimiter = ' ').reshape(-1,1) # cluster data

g_nr = gdat[:,1] - gdat[:,4] # NUV-r colours (for ordering)

cod_glst = N.array(astro_helpers.FS(g_nr, glst[:,0])[::-1]) # ordering clusters by NUV-r colours

feats = ['F-N','N-u','u-g','g-r','r-i','i-z','z-J','J-H','H-Ks'] # input feature labels

feat_glst = numpy.zeros((gdat.shape[0],len(feats)))
for i in range(len(feats)): # recalculating the input features for gswlc
    feat_glst[:,i] = gdat[:,i] - gdat[:,i+1]
trgt_glst = glst[:,0] # cluster labels

mdls = sklearn.feature_selection.SelectKBest(score_func = sklearn.feature_selection.mutual_info_classif, k = 'all') # mutual information model

fits_glst = mdls.fit(feat_glst, trgt_glst) # fitting
scrs_glst = mdls.scores_ # getting scores
scrs_glst = scrs_glst/scrs_glst.sum() # normalising
#scrs_glst = numpy.log10(scrs_glst)

fig, ax = matplotlib.subplots()

ax.set(ylim = (0,0.2), xticks = range(len(feats)), xticklabels = feats, xlabel = 'Input Features', ylabel = '$MI_{f}/\Sigma MI_{f}$')
ax.set(xlabel = 'Input Variables', ylabel = 'Relative MI Score')

ax.plot(range(len(feats)), scrs_glst, c = '#004949', ls = '-')

ax.legend(handles = [matplotlib.patches.Patch(color = '#004949', label = 'GSWLC-2')], loc = 'upper right', fontsize = 6, frameon = True, facecolor = '#ffffff', edgecolor = '#000000', framealpha = 1.0, fancybox = True, borderpad = 0.5)

fig.savefig('feat_imp.png')
