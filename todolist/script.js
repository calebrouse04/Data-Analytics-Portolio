const list = document.querySelector("ul");

function addItem() {
    const input = document.querySelector("input");
    const newItem = document.createElement("li");
    if(input.value !== ""){
        
  
    newItem.textContent = input.value;
    

    const deleteButton = document.createElement("span")
    deleteButton.textContent = "X"
    newItem.appendChild(deleteButton)
    list.appendChild(newItem);
    input.value = ""
}  }


function saveItem(){
    const items= Array.from(list.children).map(li => li.textContent.replace("X","").trim())
    localStorage.setItem("todoList", JSON.stringify(items));
    console.log(localStorage);
}

function clearItems(){
    localStorage.clear();
    while (list.firstChild) {
        list.removeChild(list.firstChild);
    }

}

const spans = document.querySelectorAll("span");



document.addEventListener("click", event => {
    if (event.target.tagName === "SPAN") {
        let listItem = event.target.parentNode; // Assume the parent is always an <li>
        list.removeChild(listItem); // Remove the list item

        
    }
});

    const inputField = document.getElementById('input');

    inputField.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {  // Check if the Enter key was pressed
            addItem()
        }
    });








    document.addEventListener("click", event => {
        if (event.target.tagName === "LI"){
            let listItem = event.target;
            
            // Toggle the textDecoration style directly
            listItem.style.textDecoration = listItem.style.textDecoration === "line-through" ? "none" : "line-through";
        }
    })