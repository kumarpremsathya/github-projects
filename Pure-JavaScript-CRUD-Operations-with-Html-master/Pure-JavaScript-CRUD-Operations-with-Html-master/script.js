var selectedRow = null;

function onFormSubmit() {
    console.log("Form submitted");
    if (validate()) {
        console.log("Form validation successful");
        var formData = readFormData();
        if (selectedRow == null) {
            console.log("Inserting new record");
            insertNewRecord(formData);
        } else {
            console.log("Updating record");
            updateRecord(formData);
        }
        resetForm();
    }
}

function readFormData() {
    console.log("Reading form data");
    var formData = {};
    formData["fullName"] = document.getElementById("fullName").value;
    formData["empCode"] = document.getElementById("empCode").value;
    formData["salary"] = document.getElementById("salary").value;
    formData["city"] = document.getElementById("city").value;
    console.log("Form data:", formData);
    return formData;
}
function insertNewRecord(data) {
    console.log("Inserting new record with data:", data);

    var table = document.getElementById("employeeList").getElementsByTagName('tbody')[0];
    console.log("Table:", table);

    var newRow = table.insertRow(table.length);
    console.log("New Row:", newRow);

    cell1 = newRow.insertCell(0);
    console.log("Cell 1:", cell1);
    cell1.innerHTML = data.fullName;
    console.log("data.fullName:", data.fullName);

    cell2 = newRow.insertCell(1);
    console.log("Cell 2:", cell2);
    cell2.innerHTML = data.empCode;
    console.log("data.empCode:", data.empCode);

    cell3 = newRow.insertCell(2);
    console.log("Cell 3:", cell3);
    cell3.innerHTML = data.salary;
    console.log("data.salary:", data.salary);

    cell4 = newRow.insertCell(3);
    console.log("Cell 4:", cell4);
    cell4.innerHTML = data.city;
    console.log("data.city:", data.city);

    cell5 = newRow.insertCell(4);
    console.log("Cell 5:", cell5);
    cell5.innerHTML = `<a onClick="onEdit(this)">Edit</a>
                       <a onClick="onDelete(this)">Delete</a>`;
}

function resetForm() {
    console.log("Resetting form");
    document.getElementById("fullName").value = "";
    document.getElementById("empCode").value = "";
    document.getElementById("salary").value = "";
    document.getElementById("city").value = "";
    selectedRow = null;
    console.log("Form reset complete");
}

function onEdit(td) {
    console.log("Editing record:", td);

    selectedRow = td.parentElement.parentElement;
    console.log("Selected Row:", selectedRow);

    document.getElementById("fullName").value = selectedRow.cells[0].innerHTML;
    console.log("Full Name value:", document.getElementById("fullName").value);

    document.getElementById("empCode").value = selectedRow.cells[1].innerHTML;
    console.log("Emp Code value:", document.getElementById("empCode").value);

    document.getElementById("salary").value = selectedRow.cells[2].innerHTML;
    console.log("Salary value:", document.getElementById("salary").value);

    document.getElementById("city").value = selectedRow.cells[3].innerHTML;
    console.log("City value:", document.getElementById("city").value);
}


function updateRecord(formData) {
    console.log("Updating record with data:", formData);
    
    console.log("Updating cell 1 with full name:", formData.fullName);
    selectedRow.cells[0].innerHTML = formData.fullName;

    console.log("Updating cell 2 with empCode:", formData.empCode);
    selectedRow.cells[1].innerHTML = formData.empCode;

    console.log("Updating cell 3 with salary:", formData.salary);
    selectedRow.cells[2].innerHTML = formData.salary;

    console.log("Updating cell 4 with city:", formData.city);
    selectedRow.cells[3].innerHTML = formData.city;

    console.log("Record updated successfully");
}


function onDelete(td) {
    console.log("Deleting record :", td);
    if (confirm('Are you sure to delete this record ?')) {
        row = td.parentElement.parentElement;
        console.log("Deleted row :", row);
        document.getElementById("employeeList").deleteRow(row.rowIndex);
        console.log("Form reset after deletion");
        resetForm();
    }
}


function validate() {
    console.log("Validating form");
    isValid = true;
    if (document.getElementById("fullName").value == "") {
        isValid = false;
        document.getElementById("fullNameValidationError").classList.remove("hide");
        console.log("Validation failed: Full Name is required");
    } else {
        isValid = true;
        if (!document.getElementById("fullNameValidationError").classList.contains("hide"))
            document.getElementById("fullNameValidationError").classList.add("hide");
        console.log("Validation successful");
    }
    return isValid;
}
