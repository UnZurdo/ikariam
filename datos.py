import json
import pandas as pd
import re
import fileinput
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

if len(sys.argv) > 1:
    if sys.argv[1] == '-A':
        for i in range(3334):
            try:
                pattern1 = re.compile('\"id\"', re.DOTALL)
                with open('json'+str(i), 'w') as out_file:
                    out_file.write("")

                with open('json'+str(i), 'a') as out_file:
                    with open('workfile'+str(i), 'r', encoding='utf8') as in_file:
                        for line in in_file:
                            if pattern1.search(line):
                                # print(line)
                                out_file.write(line)

                with fileinput.FileInput('json'+str(i), inplace=True) as out_file:
                    for line in out_file:
                        print(line.replace("ikariam.getClass(ajax.Responder, [[\"updateBackgroundData\",", ""))

                with fileinput.FileInput('json'+str(i), inplace=True) as out_file:
                    for line in out_file:
                        print(line.replace("],[\"updateTemplateData\",\"\"],[\"popupData\",null],[\"ingameCounterData\",null],[\"removeIngameCounterData\",null],[\"updateBacklink\",null]]);", ""))
            except:
                print("Error parse: " + i + "\n")
    if sys.argv[1] == '-j' or sys.argv[1] == '-A':
        ciudades = []
        duenyos = []
        niveles = []
        ali = []
        isla = []
        xcoord = []
        ycoord = []
        for i in range(3334):
            try:
                data = json.load(open('json'+str(i)))
                for city in data['cities']:
                    if city['id'] != '-1':
                        ciudades.append(city['name'])
                        niveles.append(city['level'])
                        try:
                            duenyos.append(city['ownerName'])
                        except:
                            duenyos.append("PLACEHOLDERBERTO")
                        isla.append(data['name'])
                        xcoord.append(data['xCoord'])
                        ycoord.append(data['yCoord'])
                        try:
                            ali.append(city['ownerAllyTag'])
                        except:
                            ali.append('None')
            except:
                pass
        df = pd.DataFrame(ciudades, columns=['Ciudad'])
        df['Dueño'] = duenyos
        df['Nivel'] = niveles
        df['Alianza'] = ali
        df['Isla'] = isla
        df['xCoord'] = xcoord
        df['yCoord'] = ycoord
        df[['Nivel']] = df[['Nivel']].apply(pd.to_numeric, errors='raise')
        df[['xCoord']] = df[['xCoord']].apply(pd.to_numeric, errors='raise')
        df[['yCoord']] = df[['yCoord']].apply(pd.to_numeric, errors='raise')
        # df.ix[df['Dueño'] == "PLACEHOLDERBERTO"]
        df.drop(df[df.Dueño == "PLACEHOLDERBERTO"].index, inplace=True)
        df.to_csv('dataframe.csv', encoding='utf-8')

df = pd.read_csv('dataframe.csv')
# print(df)
test = 1
test1 = ''
fig_size = []
while test != 20:
    try:
        test = int(input("Filtrar por:\n 1.Nombre colonia\n 2.Nivel colonia\n 3.Dueño\n 4.Alianza\n 5.Coordenadas\n 6.Isla\n 7.Coordenadas alianza\n 19.Test\n 20.Fin\n "))
    except:
        test = -1
    if test > 0 and test < 20:
        if test == 1:
            test1 = "Ciudad"
            test2 = input("Nombre: ")
            print("\n")
            print(df.loc[df[test1] == test2])
            print("\n\n")
        elif test == 2:
            test1 = "Nivel"
            test2 = input("Limite minimo nivel: ")
            test3 = input("Limite maximo nivel: ")
            busqueda = test1 + ' >= ' + test2 + ' and ' + test1 + '<=' + test3
            print("\n")
            sub = df.query(busqueda)
            print(sub.sort_values('Nivel', ascending=False))
            print("\n\n")
        elif test == 3:
            test1 = "Dueño"
            test2 = input("Nombre: ")
            print("\n")
            print(df.loc[df[test1] == test2])
            print("\n\n")
        elif test == 4:
            test1 = "Alianza"
            test2 = input("TAG: ")
            print("\n")
            al = df.loc[df[test1] == test2]
            with pd.option_context('display.max_rows', None):
                al = al.sort_values('Dueño', ascending=False)
                print(al.to_string(index=False))
            print("\n\n")
        elif test == 5:
            p1 = "xCoord"
            p2 = "yCoord"
            test2 = input("Limite minimo xCoord: ")
            test3 = input("Limite maximo xCoord: ")
            test4 = input("Limite minimo yCoord: ")
            test5 = input("Limite maximo yCoord: ")
            busqueda1 = p1 + ' >= ' + test2 + ' and ' + p1 + '<=' + test3
            busqueda2 = p2 + ' >= ' + test4 + ' and ' + p2 + '<=' + test5
            print("\n")
            sub = df.query(busqueda1)
            sub = sub.query(busqueda2)
            print(sub.sort_values(['xCoord', 'yCoord'], ascending=[False, False]))
            print("\n\n")
        elif test == 6:
            test1 = "Isla"
            test2 = input("Nombre: ")
            print("\n")
            print(df.loc[df[test1] == test2])
            print("\n\n")
        elif test == 7:
            p1 = "xCoord"
            p2 = "yCoord"
            test2 = input("TAG: ")
            busqueda1 = p1 + ' >= 0 and ' + p1 + '<= 100'
            busqueda2 = p2 + ' >= 0 and ' + p2 + '<= 100'
            print("\n")
            sub = df.loc[df["Alianza"] == test2]
            sub = sub.query(busqueda1)
            sub = sub.query(busqueda2)
            # with pd.option_context('display.max_rows',None):
            #    sub = sub.sort_values(['xCoord', 'yCoord'], ascending=[False, False])
            #    print(sub.to_string(index=False))
            #    print("\n\n")
            sub.to_csv(test2 + '.csv', sep=';', encoding='utf-8')
        elif test == 19:
            al1 = input("TAG1: ")
            al2 = input("TAG2: ")
            islas = df.as_matrix(columns=df.columns[5:6])
            A = np.squeeze(np.asarray(islas))
            islas = set(A)
            for isle in islas:
                sub = df.loc[df["Isla"] == isle]
                balance = 0
                control = 0
                haymiembros = 0
                for index, row in sub.iterrows():
                    ali = row['Alianza']
                    if control == 0:
                        x = row['xCoord']
                        y = row['yCoord']
                        control = 1
                    if ali == al1:
                        balance += 1
                        haymiembros += 1
                    elif ali == al2:
                        balance += -1
                        haymiembros += 1
                if balance < 0:
                    # print("Inferioridad")
                    c = 'r'
                elif balance > 0:
                    # print("Superioridad")
                    c = 'g'
                elif balance == 0 and haymiembros != 0:
                    # print("Igualdad")
                    c = 'b'
                else:
                    c = 'k'
                plt.scatter(x, y, marker='.', color=c)
            L1 = mpatches.Patch(color='g', label=al1)
            L2 = mpatches.Patch(color='r', label=al2)
            L3 = mpatches.Patch(color='b', label="Neutra")
            L4 = mpatches.Patch(color='k', label="Sin presencia")
            plt.legend(handles=[L1, L2, L3, L4])
            # plt.grid()
            plt.show()
    elif test == 20:
        print("Finalizando...")
    else:
        print("\nParametro invalido\n")

# df.to_csv('data.csv', sep=';', encoding='iso-8859-1')
