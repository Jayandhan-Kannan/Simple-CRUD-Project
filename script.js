function createBook() 
{
    var name = document.getElementById("name").value;
    var number = document.getElementById("number").value;
    var author = document.getElementById("author").value;
    var rating = document.getElementById("rating").value;

    const apiUrl = `http://127.0.0.1:8000/create`; 

    var bookData = {
        book_name: name,
        book_number: number,
        book_author: author,
        book_rating: rating
    };

    fetch(apiUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(bookData)
    })

    .then(response => { 
        if(response.ok)
        {
            document.getElementById("create").innerHTML = "Book Details Added Successfully"
        }
        else
        {
            if(response.status = 422)
            {
                document.getElementById("create").innerHTML = "Please provide data as per condition"
            }
        }
        return response.json() 
    })

    .then(data => {
        console.log("Response data : ",data)
    })

    .catch(error => {
        document.getElementById("create").innerText = "Error adding book details";
        console.error("Error:", error);
    });
}

function getBookByNo()
{
    var bookNumber = document.getElementById("bno").value;

    const apiUrl = `http://127.0.0.1:8000/book/${encodeURIComponent(bookNumber)}`;

    fetch(apiUrl, {
        method: "GET",
        headers:{
            "Content-Type": "application/json"
        }
    })

    .then(response => {
        console.log(response.status)
        if(response.status == 204)
        {
            document.getElementById("getbyno").innerHTML = `<h4>Book Not Found for this Number</h4>`
        }
        else
        {
            document.getElementById("getbyno").innerHTML = `<h3>Please provide data</h3>`
        }
        return response.json();
    })

    .then(data=> {
        console.log(data.message)
        document.getElementById("getbyno").innerHTML = `
            <p><strong>Book Number : </strong> ${data.book_number}</p>
            <p><strong>Book Name : </strong> ${data.book_name}</p>  
            <p><strong>Book Author : </strong> ${data.book_author}</p> 
            <p><strong>Book Rating : </strong> ${data.book_rating}</p> 
        `;
    })
    
    // .catch(error=>{
    //     document.getElementById("getbyno").innerHTML = `Failed to fetch details: ${error.message}`;
    //     console.log("Error : ", error);
    // })   
}

function getAllBooks()
{
    const tableBody = document.getElementById("tbody");
    
    const apiUrl = `http://127.0.0.1:8000/books`;

    fetch(apiUrl,{
        method:"GET",
        headers:{
            "Content-Type": "application/json"
        }
    })

    .then(response =>{
        console.log(response.status)
        if(response.status == 204)
        {
            document.getElementById("tbody").innerHTML = `<Strong>No records available</Strong>`
        }
        else
        {
            console.log("No records available")
        }
        return response.json();
    })

    .then(data => {
        tableBody.innerHTML = '';
        console.log(data);
        data.forEach(element => {
            const newRow = document.createElement("tr");
            newRow.innerHTML =`
            <td>${element.book_number}</td>
            <td>${element.book_name}</td>
            <td>${element.book_author}</td>
            <td>${element.book_rating}</td>
            `;
            tableBody.appendChild(newRow);
        })
    })

    // .catch(error=>{
    //     document.getElementById("allbookerror").innerHTML = `Failed to fetch details: ${error.message}`;
    //     console.log("Error : ", error);
    // })
}

function updateBook()
{
    var name = document.getElementById("uname").value;
    var number = document.getElementById("unumber").value;
    var author = document.getElementById("uauthor").value;
    var rating = document.getElementById("urating").value;
    var bnumber = document.getElementById("bnumber").value;

    const apiUrl = `http://127.0.0.1:8000/update/${encodeURIComponent(bnumber)}`; 

    var bookData = {
        book_name: name,
        book_number:number,
        book_author: author,
        book_rating: rating
    };

    fetch(apiUrl, {
        method:"PUT",
        headers:{
            "Content-Type":"application/json"
        },
        body: JSON.stringify(bookData) 
    })

    .then(response => {
        if(response.ok)
        {
            document.getElementById("update").innerHTML = "Updated successfully"
        }
        else
        {
            if(response.status == 404)
            {
                document.getElementById("update").innerHTML = "Updation failed"
            }
            else
            {
                document.getElementById("update").innerHTML = "Please provide data"
            }
            
        }
        return response.json()
    })

    .then(data => {
        console.log(data)
    })
}

function deleteBook()
{
    var number = document.getElementById("dnumber").value;

    const apiUrl = `http://127.0.0.1:8000/delete/${encodeURIComponent(number)}`;

    fetch(apiUrl,{
        method:"DELETE",
        headers:{
            "Content-Type":"application/json"
        }
    })

    .then(response => {
        console.log(response.status)
        if(response.ok)
        {
            document.getElementById("delete").innerHTML = `<h3>Book deleted successfully</h3>`
        }
        else
        {
            document.getElementById("delete").innerHTML = "<h3>Book Not Available for this Number</h3>"
        }
        return response.json()
    })

    .then(data => {
        console.log(data)
    })


}