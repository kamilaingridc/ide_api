from fastapi import FastAPI, HTTPException, status, Response, Path
from typing import Optional
from modelo import IDES

app = FastAPI()

ides = {
    1: {
        "nome": "Visual Studio (VS Code)",
        "versao": 1.87,
        "linguagem": "C#, Visual Basic.NET, C++, F#, JavaScript, TypeScript, Python, entre outros.",
        "image:": "C:/Users/50252782879/Desktop/ide_api/images/vsCode_.png"
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
    }
}

# GET 
@app.get('/')
async def root():
    return {"message": "its working"}

@app.get('/ides/{ide_id}')
async def get_ides(ide_id: int = Path(..., title='ide id', description='must be an integer', gt=0, lt=7)):
    try:   
        ide = ides[ide_id]
        return ide
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="IDE not found.")

# POST 
@app.post('/ides', status_code=status.HTTP_201_CREATED)
async def post_ide(ide:IDES):
    if ide.id not in ides:
        next_id = len(ides) + 1
        ides[next_id] = ide
        del ide.id
        return ide
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'already exist id {ide.id}')

# PUT
@app.put('/ides/{ide_id}',)
async def put_ide(ide_id:int, ide:IDES):
    if ide_id in ides:
        ides[ide_id] = ide
        del ide.id
        return ide
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'dont exist an ide w the id {ide_id}.')
    
# DELETE 
@app.delete('/ides/{ide_id}')
async def delete_ide(ide_id: int):
    if ide_id in ides:
        del ides[ide_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'dont have an ide w the id {ide_id}.')

# PATCH - mesmo fim que a put
# substitui um pedaço
@app.patch('/ides/{ide_id}')
async def patch_ide(ide_id: int, ide: IDES):
    if ide_id in ides:
        ides[ide_id].update(ide)
        return ides[ide_id]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'dont have an ide w the id {ide_id}.')

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)
