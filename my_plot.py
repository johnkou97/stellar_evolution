import scienceplots
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

tex_fonts = {"axes.labelsize": 12,
	"font.size": 12,
	# Make the legend/label fonts a little smaller
	"legend.fontsize": 10,
	"xtick.labelsize": 10,
	"ytick.labelsize": 10,
	}



CORNER_KWARGS = dict(
	#     smooth=0.9,
	#     label_kwargs=dict(fontsize=16),
	#     title_kwargs=dict(fontsize=16),
	quantiles=[0.16, 0.50, 0.84],
	levels=[0.20, 0.40, 0.85, 0.99],#(1 - np.exp(-0.5), 1 - np.exp(-2), 1 - np.exp(-9 / 2.)),
	plot_density=False,
	plot_datapoints=False,
	fill_contours=True,
	show_titles=False,
	#     max_n_ticks=3,
	title_fmt=".2E"
	)

def set_size(width, fraction=1, subplots=(1, 1)):
	"""Set figure dimensions to avoid scaling in LaTeX.

	Parameters
	----------
	width: float or string
			Document width in points, or string of predined document type
	fraction: float, optional
			Fraction of the width which you wish the figure to occupy
	subplots: array-like, optional
			The number of rows and columns of subplots.
	Returns
	-------
	fig_dim: tuple
			Dimensions of figure in inches
	"""
	# if width == 'thesis':
	# 	width_pt = 426.79135
	# elif width == 'beamer':
	# 	width_pt = 307.28987
	# else:
	width_pt = width

	# Width of figure (in pts)
	fig_width_pt = width_pt * fraction
	# Convert from pt to inches
	inches_per_pt = 1 / 72.27

	# Golden ratio to set aesthetic figure height
	# https://disq.us/p/2940ij3
	golden_ratio = (5**.5 - 1) / 2

	# Figure width in inches
	fig_width_in = fig_width_pt * inches_per_pt
	# Figure height in inches
	fig_height_in = fig_width_in * golden_ratio * (subplots[0] / subplots[1])

	return (fig_width_in, fig_height_in)

def plot_thesis(trace,t,rv_obs,rv_err,t_plot,name,loc='images',form='pdf'):
	latex_size=set_size(390.0)
	
	with mpl.style.context('science'):
		plt.rcParams.update(tex_fonts)
		plt.figure(figsize=latex_size)
		rv_plot = trace.posterior["rv_plot"].values
		q16, q50, q84 = np.percentile(rv_plot, [16, 50, 84], axis=(0, 1))
		plt.errorbar(t, rv_obs, yerr=rv_err, fmt=".k", label="data")
		plt.plot(t_plot, q50)
		plt.fill_between(t_plot, q16, q84, alpha=0.3, label="posterior")
		plt.xlim(0, 130)
		plt.legend()#,bbox_to_anchor=(0.30,0.86))
		plt.xlabel(r'Time (days)')
		plt.ylabel(r'Radial Velocity (m/s)')
		plt.savefig(f'{loc}/rv-t_{name}.{form}',dpi=600,bbox_inches='tight')
		plt.close()


def plot_corner(trace,name,loc='images',form='pdf'):
	corner_latex=set_size(390,subplots=(2,2))

	with mpl.style.context('science'):
		plt.rcParams.update(tex_fonts)
		fig=corner.corner(trace, var_names=['period','ecc'],labels=[r'period (days)',r'eccentricity'],**CORNER_KWARGS)
		fig.set_size_inches(corner_latex[0],corner_latex[1]*1.5)
		plt.savefig(f'{loc}/corner_{name}.{form}',dpi=600,bbox_inches='tight')
		plt.close()


def plot_contour(rv_max,t_roch,moon_period,moon_mass,solar_mass,ear_mass,x_pos,y_pos,kep1708,kep1625,hill_sphere = 0,name='contourPlot'
	,loc='Contour_Plots',form='png'):

	latex_size=set_size(390.0)

	with mpl.style.context('science'):
		plt.rcParams.update(tex_fonts)

		X = moon_period
		# print(X)
		Y = moon_mass*solar_mass/ear_mass
		plt.figure(figsize=latex_size)
		plt.contourf(X,Y,rv_max)
		cb = plt.colorbar()
		cb.set_label(label='Peak Radial Velocity (m/s)')
		CS=plt.contour(X,Y,rv_max,levels=[500],linestyles='--',colors='white')
		positions = [(1,35)]
		# plt.clabel(CS,fmt='500m/s', inline=False, inline_spacing=1,use_clabeltext=True,colors='C3',fontsize='15')
		label = plt.clabel(CS,fmt='500m/s', inline=False,rightside_up=False,colors='C3',fontsize='15',manual=positions)
		for l in label:
			l.set_rotation(20)
		# CS=plt.contour(X,Y,rv_max,levels=[250],linestyles='--',label='250m/s',fontsize='15')
		# plt.clabel(CS,fmt='250/s', inline=False, inline_spacing=1,use_clabeltext=True,colors='C3',fontsize='15')
		# plt.plot(t_roch,moon_mass*solar_mass/ear_mass,color='orange',linestyle='--',label='Roche Limit')
		plt.fill_between(t_roch,moon_mass[-1]*solar_mass/ear_mass,moon_mass*solar_mass/ear_mass,color='grey')
		plt.text(.15,70,'Roche limit',fontsize='15',rotation=90)
		plt.scatter(kep1708[0],kep1708[1],label='Kepler-1708 b-i',marker='o',color='snow')
		plt.scatter(kep1625[0],kep1625[1],label='Kepler-1625 b-i',marker='o',color='gold')
		plt.scatter(x_pos,y_pos,label='RV detection limit',marker='+',color='cyan')
		if hill_sphere != 0:
			plt.vlines(hill_sphere,moon_mass[0]*solar_mass/ear_mass,moon_mass[-1]*solar_mass/ear_mass,color='olive'
				,linestyle='--',label='Hill sphere limit')
			# plt.legend(frameon=True,loc='center right')
		# else:
			# plt.legend(frameon=True,loc='upper left')
		plt.xscale('log')
		plt.xlim(moon_period[0],moon_period[-1])
		plt.ylim(moon_mass[0]*solar_mass/ear_mass,moon_mass[-1]*solar_mass/ear_mass)
		plt.xlabel('Orbital Period (days)')
		plt.ylabel(r'Moon Mass ($M_\oplus$)')
		plt.tick_params(which='both',color='red')
		plt.savefig(f'{loc}/{name}.{form}',dpi=600,bbox_inches='tight')
		plt.close()



# if __name__ == '__main__':
	