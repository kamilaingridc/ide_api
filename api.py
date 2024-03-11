from fastapi import FastAPI, HTTPException, status, Response, Path
from fastapi.encoders import jsonable_encoder
from modelo import IDES

app = FastAPI()

ides = {
    "1": {
        "nome": "Visual Studio (VS Code)",
        "versao": 1.87,
        "linguagem": "C#, Visual Basic.NET, C++, F#, JavaScript, TypeScript, Python, entre outros.",
        "imagem": "https://cdn.worldvectorlogo.com/logos/visual-studio-code-1.svg"
    },
    "2": {
        "nome": "Eclipse",
        "versao": 2019.09,
        "linguagem": "Popularmente usada para desenvolvimento Java, mas também suporta outras linguagens através de plug-ins, como C/C++, Python, PHP e Ruby.",
        "imagem": "https://www.perforce.com/sites/default/files/image/2017-05/image-body-integrations-eclipse_0.png"
    },
    "3": {
        "nome": "IntelliJ IDEA",
        "versao": 2023.3,
        "linguagem": "Poderosa para desenvolvimento Java, mas também suporta outras linguagens como Kotlin, Groovy, Scala e JavaScript.",
        "imagem": "https://logowik.com/content/uploads/images/jetbrains-intellij-idea6941.jpg"
    },
    "4": {
        "nome": "PyCharm",
        "versao": 2023.3,
        "linguagem": "Específica para Python, com suporte para frameworks populares como Django e Flask, além de outras tecnologias relacionadas a Python, como Jupyter Notebooks.",
        "imagem": "https://logowik.com/content/uploads/images/pycharm6005.logowik.com.webp"
    },
    "5": {
        "nome": "Xcode",
        "versao": 15,
        "linguagem": "Desenvolvimento de aplicativos para iOS, macOS, watchOS e tvOS, principalmente usando Swift e Objective-C.",
        "imagem": "https://upload.wikimedia.org/wikipedia/en/5/56/Xcode_14_icon.png"
    }
}

# GET 
@app.get('/ides')
async def root():
    return ides

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
@app.patch('/ides/{ide_id}', response_model=IDES)
async def patch_ide(ide_id: str, ide: IDES):
    if ide_id in ides:
        stored_item_data = ides[ide_id]
        stored_item_model = IDES(**stored_item_data)
        del stored_item_model.id
        update_data = ide.model_dump(exclude_unset=True)
        updated_item = stored_item_model.model_copy(update=update_data)
        ides[ide_id] = jsonable_encoder(updated_item)
        return updated_item
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'dont have an ide w the id {ide_id}.')

if __name__ == "__main__":
    import uvicorn
    
# ip do pc 
    uvicorn.run("api:app", host="10.234.87.157", port=8000, log_level="info", reload=True)
