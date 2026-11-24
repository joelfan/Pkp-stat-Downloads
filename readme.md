################################################################################
# Program to compute downloads for any OJS or OMP platform for a specific year #
#                                                                              #
# This program must be launched with the following mandatory parameters:       #
# python pkpDownloads.py DESTURL YEAR OUTFILE APIKEY                           #
# 																			   #
# where:                                                                       #
#       - DESTURL is in the form https://ojs.example.com                       #
#       - YEAR    is the year in the form aaaa (2026 for example)              #
#       - OUTFILE is the suffix of the output file                             #
#       - APIKEY  is the APIKEY                                                #
# 																			   #
# The program must be launched for each platform. So, if you have OJS and OMP, #
#   you should lauch twice, in the following forms:                            #
#	python pkpDownloads.py https://ojs.example.com 2025 outOjs ojsApiKey	   #
#	python pkpDownloads.py https://omp.example.com 2025 outOmp ompApiKey 	   #
# 																			   #
# 																			   #
# The program produces two output files for each launch, in json format.	   #
# One file contains the series, and the other one contains the series with     #
# related statistics 														   #
# 																			   #
# 																			   #
#                                                            2026 Dario Basset #
################################################################################