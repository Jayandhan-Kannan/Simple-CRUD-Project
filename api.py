from typing import Optional
from fastapi import FastAPI, HTTPException, Path, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
import pymysql
import pymysql.cursors

description = """
**This is a Basic CRUD Operations - API for Book Store**.

## Operations

User can perform **CRUD**.
* **Create Books** 

* **Retrieve Books** 

* **Update Books** 

* **Delete Books** 

## Benefits

You will be able to:

* **Maintain Records Digitally** 

* **Reduce Manwork**

* **Reduce Resources** 

* **Enhance Security** 

* **Easy Accessible and Editable** 
"""

app = FastAPI(
    title="Book Store API",
    description=description,
    version="1.0.0",
)

# templates = Jinja2Templates(directory=str(Path("D:/Jayandhan/api/templates")))

origins = [
    "http://localhost:3000",  # Your frontend origin
    "http://127.0.0.1:3000",
    "null",  # Allows requests from 'null' origins, e.g., local file access
]

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials = True, allow_methods=["*"], allow_headers=["*"]
)

# Database custom error
class DatabaseConnectionError(Exception):
    pass
@app.exception_handler(DatabaseConnectionError)
async def database_exception_handler(request: Request, exc: DatabaseConnectionError):
    return JSONResponse(
        status_code=500,
        content={"error": "Unable to connect with database"}
    )

def connect_to_db():
    try:
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="*Kj@1512*",
            database="college",
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MYSQLError as e:
        return None

class Book(BaseModel):
    book_name: str = Field(min_length=3, max_length=50, example="Harry Potter")
    book_number: int = Field(lt=500, gt=100, example="101")
    book_author: str = Field(min_length=3, max_length=30, example="James Williams")
    book_rating:int = Field(lt=6,gt=0,example="5")


@app.get(
            "/test",
            summary="Sample Test call",
        )
async def test():
    return{"message":"test call"}

@app.post(
            "/create",
            summary="Create a New Book Details",
            description="This API Endpoint is used to create a new book details with custom parameters",
            responses={
                200: {"description":"Book Details Added Successfully"},
                422: {"description":"Failed to added, Please provide data based on constraints"},
            },
            tags=["Create"]
        )
async def create_books(book:Book):
    connection = connect_to_db()
    if not connection:
        raise DatabaseConnectionError()
    
    try:
        with connection.cursor() as cursor:
            sql = "CALL spCreateBook(%s, %s, %s, %s);"
            cursor.execute(sql, (book.book_name, book.book_number, book.book_author, book.book_rating))
            connection.commit()

            return{"message":"Book details added successfully"}
    except pymysql.MySQLError as e:
        raise DatabaseConnectionError()
    finally:
        if connection:
            connection.close()
    

@app.get(
            "/book/{no}",
            summary="Retrieve a Book Using Book Number",
            description="This API Endpoint is used to retrieve a book details using book number",
            responses={
                    200: {"description":"Book Details Retrieved Successfully"},
                    422: {"description":"Failed to retrieve, Please provide data based on constraints"},
                },
            tags=["Retrieve"]
        )
async def get_book_by_no(no: int=Path(description="Book number of the book to retrieve",example="101")):
    connection = connect_to_db()
    if not connection:
        raise DatabaseConnectionError()    
    
    try:
        with connection.cursor() as cursor:
            sql = "CALL spGetBook(%s);"
            cursor.execute(sql, (no),)
            result = cursor.fetchone()
            if result:
                return result
            else:
                raise HTTPException(status_code=204, detail="No data found")
    except pymysql.MySQLError as e:
        print(f"Error fetching the details: {e}")
        raise DatabaseConnectionError()
    finally:
        if connection:
            connection.close()
    
        
@app.get(   
        "/books",
        summary="Retrieve All Books",
        description="This API Endpoint is used to retrieve all book details",
        responses={
                200: {"description":"Book Details Retrieved Successfully"},
            },
        tags=["Retrieve"]
        )
async def get_all_books():
    connection = connect_to_db()
    if not connection:
        raise DatabaseConnectionError()
    
    try:
        with connection.cursor() as cursor:
            sql = "CALL spGetAllBooks();"
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                return result
            else:
                raise HTTPException(status_code=204, detail="No data found")
    except pymysql.MySQLError as err:
        print(f"Error fetching Books: {err}")
        raise DatabaseConnectionError()
    finally:
        if connection:
            connection.close()

@app.put(
            "/update/{no}",
            summary="Update a Book Using Book Number",
            description="This API Endpoint is used to update a book details using book number",
            responses={
                    200: {"description":"Book Details Updated Successfully"},
                    422: {"description":"Failed to update, Please provide data based on constraints"},
                },
            tags=["Update"]
        )
async def update_book(book:Book, no:int=Path(description="Book number of the book to update",example="101")):
    connection = connect_to_db()
    if not connection:
        raise DatabaseConnectionError()
    
    try:
        with connection.cursor() as cursor:
            sql = "CALL spUpdateBook(%s, %s, %s, %s);"
            cursor.execute(sql, (book.book_name, no, book.book_author, book.book_rating))
            connection.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Updation failed")

            return {"message": f"Book Details with book number {no} updated successfully"}
    except pymysql.MySQLError as e:
        print(f"Error updating book: {e}")
        raise DatabaseConnectionError()
    finally:
        if connection:
            connection.close()
    
        
@app.delete(
            "/delete/{no}",
            summary="Delete a Book Using Book Number",
            description="This API Endpoint is used to delete a book details using book number",
            responses={
                    200: {"description":"Book Deleted Updated Successfully"},
                    422: {"description":"Failed to delete, Please provide data based on constraints"},
                },
            tags=["Delete"]
        )
async def delete_book(no:int=Path(description="Book number of the book to delete",example="101")):
    connection = connect_to_db()
    if not connection:
        raise DatabaseConnectionError()
    try:  
        with connection.cursor() as cursor:
            sql = "CALL spDeleteBook(%s);"
            cursor.execute(sql, (no,))
            connection.commit()
            if(cursor.rowcount == 0):
                raise HTTPException(status_code=404, detail="Book not found")
            return{"message":"deleted successfully"}
    except pymysql.MySQLError as e:
        print(f"error occured: {e}")
        raise DatabaseConnectionError()
    finally:
        if connection:
            connection.close()
        

