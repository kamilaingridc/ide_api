# importa bibliotecas
from fastapi import FastAPI  
from model import Pokemons
from fastapi import HTTPException, status, Response, Path, Header, Depends
from typing import Optional, Any, List
from time import sleep

def fake_bd():
    try:
        print("Abrindo o banco de dados.")
        sleep(1)
    finally:
        print("Fechando o banco de dados.")
        sleep(1)

app = FastAPI(title='API de algumas IDEs.', version='0.0.1', description="Exemplos de IDEs.")  # instancia a biblioteca

ides = {
    1: {
        "nome": "Visual Studio",
        "versao": 1.87,
        "linguagem": "C#, Visual Basic.NET, C++, F#, JavaScript, TypeScript, Python, entre outros."
    },
    2: {
        "nome": "Eclipse",
        "versao": 2019.09,
        "linguagem": "Popularmente usada para desenvolvimento Java, mas também suporta outras linguagens através de plug-ins, como C/C++, Python, PHP e Ruby."
    },
    3: {
        "nome": "IntelliJ IDEA",
        "versao": 2023.3,
        "linguagem": "Poderosa para desenvolvimento Java, mas também suporta outras linguagens como Kotlin, Groovy, Scala e JavaScript."
    },
    4: {
        "nome": "PyCharm",
        "versao": 2023.3,
        "linguagem": "Específica para Python, com suporte para frameworks populares como Django e Flask, além de outras tecnologias relacionadas a Python, como Jupyter Notebooks."
    },
    5: {
        "nome": "Xcode",
        "versao": 15,
        "linguagem": "Desenvolvimento de aplicativos para iOS, macOS, watchOS e tvOS, principalmente usando Swift e Objective-C."
    },
    6: {
        "nome": "Android Studio",
        "versao": 4.2,
        "linguagem": "Oficial para desenvolvimento de aplicativos Android."
    },
    7: {
        "nome": "NetBeans",
        "versao": 12.3,
        "linguagem": "Código aberto que suporta várias linguagens, incluindo Java, PHP, C/C++, e HTML5/JavaScript."
    },
    8: {
        "nome": "Sublime Text",
        "versao": 4114,
        "linguagem": "Altamente personalizável."
    }
}

@app.get("/")  # pega pra mostrar o caminho
async def raiz():  # função assíncrona
    return{"Mensagem": 'Deu certo :P'}  # retorna mensagem

@app.get("/pokemon", description='retorna um alista de pokemns cadastrados ou uma lista vazia.', response_model=List[Pokemons])
async def get_pokemons(db: Any = Depends(fake_bd)): # retorna todos os pokemons 
    return pokemons


@app.get('/pokemon/{pokemon_id}')
async def get_pokemon(pokemon_id: int = Path(..., title='pegar o pokemon pelo id', gt=0, lt=3, description='selecionar pokemon pelo id onde o id deve ser 1 ou 2')):
    if pokemon_id not in pokemons:  # return a message for false id 
        raise HTTPException (status_code=404, detail="Pokemon não encontrado.")
    return pokemons[pokemon_id]

# POST 
@app.post('/pokemon', status_code=status.HTTP_201_CREATED)
async def post_pokemon(pokemon: Optional[Pokemons] = None):  # 
    if pokemon.id not in pokemon:
        next_id = len(pokemons) + 1
        pokemons[next_id] = pokemon
        del pokemon.id
        return pokemon
    
    else: 
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Já existe um pokemon com esse id')

# atualiza    
@app.put('/pokemon/{pokemon_id}',)
async def put_pokemon(pokemon_id: int, pokemon: Pokemons):
    if pokemon_id in pokemons:
        pokemons[pokemon_id] = pokemon
        pokemon.id = pokemon_id
        del pokemon.id      # atualiza os dados 
        return pokemon
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não existe pokemon com id {pokemon_id}')
    
# delete
@app.delete('/pokemon/{pokemon_id}')
async def delete_pokemon(pokemon_id: int):
    if pokemon_id in pokemons:
        del pokemons[pokemon_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não existe pokemon com id {pokemon_id}')
    
#############################################
@app.get('/calculadora/soma')
async def calcular(n1:int, n2:int, n3:Optional[int]= None):
    if n3 == None:
        resultado = n1 + n2 
        return {resultado}
    else:
        resultado = n1 + n2 + n3
        return {resultado}
    
@app.get('/calculadora/subtracao')
async def calcular(n1:int, n2:int, n3:Optional[int]= None):
    if n3 == None:
        resultado = n1 - n2 
        return {resultado}
    else:
        resultado = n1 - n2 - n3
        return {resultado}
    
@app.get('/calculadora/multiplicacao')
async def calcular(n1:int, n2:int, n3:Optional[int]= None):
    if n3 == None:
        resultado = n1 * n2 
        return {resultado}
    else:
        resultado = n1 * n2 * n3
        return {resultado}
    
@app.get('/calculadora/divisao')
async def calcular(n1:int, n2:int, n3:Optional[int]= None):
    if n3 == None:
        resultado = n1 / n2 
        return {resultado}
    else:
        resultado = n1 / n2 / n3
        return {resultado}
#############################################

#############################################
@app.get('/headerEx')
async def headerEx(wilson: str = Header(...)):
    return {f'Wilson': (wilson)}
#############################################


# roda o servidor
if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port = 8000, log_level = "info", reload=True)
