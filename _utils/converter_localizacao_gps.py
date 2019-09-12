
#CONVERTE AS COORDENAS EM POSIÇÃO GPS
def coordenadas_em_gps(p_coordenadas, p_mapa):
        p_mapa = p_mapa.lower()
        #DIVIDE O RETORNO PARA AS COORDENADAS X Y Z
        pos = p_coordenadas.split()
        x = pos[0]
        y = pos[1]
        #z = pos[2]

        p_mapa = p_mapa.replace(' ', '_')
        p_mapa = p_mapa.lower()

        #SELECIONA O MAPA CORRETO PARA A CONVERSÃO
        if (p_mapa == 'ragnarok'):
            var_x = 13100
            var_y = 13100

        elif (p_mapa == 'the_island' or p_mapa == 'scorched_earth' or  p_mapa == 'aberration' or  p_mapa == 'extinction' ):
            var_x = 8000
            var_y = 8000

        elif (p_mapa == 'valguero'):
            var_x == 8160
            var_y == 8160
            
        elif (p_mapa == 'olympus'):
            var_x = 25700
            var_y = 19450

        #REALIZA A CONVERSÃO DOS DADOS COM BASE NA ESPECIFICAÇÃO DO MAPA
        latitude =  round((float(y[2:]) / var_x) + 50, 2)
        longitude = round((float(x[2:]) / var_y) + 50, 2)
        r_gps = []
        r_gps.append(latitude)
        r_gps.append(longitude)

        return r_gps

if __name__=='__main__':
    print(coordenadas_em_gps('X=-108969.844 Y=-204875.094 Z=50018.527', 'ragnarok'))