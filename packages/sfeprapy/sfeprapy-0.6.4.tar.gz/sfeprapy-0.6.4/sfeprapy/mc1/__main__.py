if __name__ == '__main__':
    import sys
    import warnings
    import sfeprapy.mc1.mc1 as mc1

    warnings.filterwarnings('ignore')

    if len(sys.argv) > 1:
        mc1.main(sys.argv[1])
    else:
        mc1.main()
