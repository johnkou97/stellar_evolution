tex_fonts = {"axes.labelsize": 12,
	"font.size": 12,
	"legend.fontsize": 10,
	"xtick.labelsize": 10,
	"ytick.labelsize": 10,
	}

def set_size(width, fraction=1, subplots=(1, 1)):
	'''
	Set figure dimensions to avoid scaling in LaTeX.
	'''
	width_pt = width

	# Width of figure (in pts)
	fig_width_pt = width_pt * fraction
	# Convert from pt to inches
	inches_per_pt = 1 / 72.27

	# Golden ratio 
	golden_ratio = (5**.5 - 1) / 2

	# Figure width in inches
	fig_width_in = fig_width_pt * inches_per_pt
	# Figure height in inches
	fig_height_in = fig_width_in * golden_ratio * (subplots[0] / subplots[1])

	return (fig_width_in, fig_height_in)

	