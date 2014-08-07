#coding: utf-8
import gdal, time, numpy, sys, os
from gdalconst import *

driver = gdal.GetDriverByName('GTiff')
driver.Register()

nome = 'empilhada'
extensao = '.tif'

entrada = gdal.Open(nome+extensao,GA_ReadOnly)
if  entrada is None:
    print 'Erro ao abrir o arquivo: ' + nome+extensao
    sys.exit(1)

linhas = entrada.RasterYSize
colunas = entrada.RasterXSize
NBandas = entrada.RasterCount
driverEntrada = entrada.GetDriver()
projecao = entrada.GetProjection()

print 'linhas:',linhas,' colunas:',colunas,'bandas:',NBandas,'driver:',driverEntrada.ShortName

#----------

def saidaImagem(img,rows,cols,bandas):
	saida = driver.Create(nome+str(rows)+'x'+str(cols)+extensao,cols,rows,bandas,GDT_Byte)
	if saida is None:
		print 'Erro ao criar o arquivo: ' + nome+extensao
		sys.exit(1)

	saida.SetProjection(projecao)
	
	for i in range(0,NBandas):
		banda = saida.GetRasterBand(i+1)
		banda.WriteArray(img.GetRasterBand(i+1).ReadAsArray(0,0,cols,rows),0,0)
		banda = None
		print 'Banda'+str(i+1)+' escrita.'
	saida = None
	print 'Imagem Pronta'

saidaImagem(entrada,linhas-6000,colunas-6000,NBandas)