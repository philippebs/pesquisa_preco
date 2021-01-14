#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 GTB7.1 (.NET CLR 3.5.30729)", "Referer": "http://example.com"}

submarino = 'https://www.submarino.com.br'
americanas = 'https://www.americanas.com.br'


def separador(produto, imprime_nome_produto = False):
	print('*' * len(produto), end='')

	if imprime_nome_produto:
		print('\n' + produto)


def buscar_americanas(site, busca):
	separador(site.split('.')[1].upper(), True)
	response = requests.get(site + '/busca/' + busca, headers=headers, timeout=10)
	soup = BeautifulSoup(response.content, 'html.parser')

	sections = soup.find_all('div', attrs={'class' : 'src__Wrapper-sc-1k0ejj6-2 dGIFSc'})
	if len(sections) > 0:
		ultimo_produto = ''
		for section in sections:
			tag_a = section.find('a')
			nome = tag_a.find('span', attrs={'class': 'src__Text-sc-154pg0p-0 src__Name-sc-1k0ejj6-3 dSRUrl'})
			preco = tag_a.find('span', attrs={'class': 'src__Text-sc-154pg0p-0 src__PromotionalPrice-sc-1k0ejj6-7 iIPzUu'})
			
			ultimo_produto = nome.string
			separador(ultimo_produto, True)
			print(preco.text.split( )[1])
			print(site + tag_a.get('href') + '\n')
		separador(ultimo_produto)
	else:
		print('Produto "%s" não encontrado.\n' % busca)


def buscar_submarino(site, busca):
	separador(site.split('.')[1].upper(), True)

	response = requests.get(site + '/busca/' + busca, headers=headers, timeout=10)

	#soup = BeautifulSoup(response.content, 'html5lib')
	soup = BeautifulSoup(response.content, 'html.parser')
	sections = soup.find_all('div', attrs={'class' : 'RippleContainer-sc-1rpenp9-0 dMCfqq'})
	if len(sections) > 0:
		ultimo_produto = ''
		for section in sections:
			tag_a = section.find('a')
			h2 = tag_a.find('h2', attrs={'class': 'TitleUI-sc-1f5n3tj-13 dTabgr TitleH2-sc-1wh9e1x-1 fINzxm'})
			preco = tag_a.find('span', attrs={'class': 'PriceUI-sc-1f5n3tj-9'})
			
			ultimo_produto = h2.text
			separador(ultimo_produto, True)
			print(preco.text.split( )[1])
			print(site + tag_a.get('href') + '\n')
		separador(ultimo_produto)
	else:
		print('Produto "%s" não encontrado.\n' % busca)


if __name__ == "__main__":
	pesquisa = input("Qual o produto que gostaria de pesquisar? ")
	buscar_submarino(submarino, pesquisa)
	buscar_americanas(americanas, pesquisa)

