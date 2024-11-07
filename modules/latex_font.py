import matplotlib.pyplot as plt

def latex_font(): 
    plt.rcParams.update({
        'text.usetex': True,
        'font.family': 'serif',
        'font.size': 12
    })
    
def latex_font1(): # Aesthetic choice
    import matplotlib as mpl
    import matplotlib.font_manager as font_manager
    plt.rcParams.update({
        'font.family': 'serif',
        'mathtext.fontset': 'cm',
        'axes.unicode_minus': False,
        'axes.formatter.use_mathtext': True,
        'font.size': 12
    })
    cmfont = font_manager.FontProperties(fname=mpl.get_data_path() + '/fonts/ttf/cmr10.ttf')

def latex_font2(): 
    plt.rcParams.update({
        'text.usetex': True,
        'font.family': 'serif',
        'font.size': 12
    })
latex_font2()