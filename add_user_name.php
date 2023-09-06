<!DOCTYPE html>
<html>
<head>
	<title>Add User &amp; Cards</title>
	<style>
		body {
			background-color: lightgreen;
		}
		form {
			display: flex;
			flex-direction: column;
			align-items: center;
			margin-top: 50px;
		}
		input[type=text] {
			padding: 10px;
			margin: 5px;
			border: none;
			border-radius: 5px;
			box-shadow: 1px 1px 1px gray;
		}
		input[type=submit] {
			padding: 10px;
			margin: 5px;
			border: none;
			border-radius: 5px;
			background-color: darkgreen;
			color: white;
			font-weight: bold;
			box-shadow: 1px 1px 1px gray;
			cursor: pointer;
		}
	</style>
</head>
<body>
	<h1>Add User &amp; Cards</h1>
	<form method="get" action="adduser.php">
		<label for="fname">First Name:</label>
		<input type="text" id="fname" name="fname" required>

		<label for="lname">Last Name:</label>
		<input type="text" id="lname" name="lname" required>

		<input type="submit" value="Submit" onclick="return validateForm();">
	</form>

	<script>
		function validateForm() {
			var fname = document.getElementById("fname").value;
			var lname = document.getElementById("lname").value;
			if (fname.trim() == "" || lname.trim() == "") {
				alert("First name and last name cannot be blank.");
				return false;
			}
			return true;
		}
	</script>
</body>
</html>
