const login = async (username, password) =>{
	let params = new URLSearchParams({
		username,
		password,
	})

	return await fetch("/auth/login", {
		body: params,
		headers: {
		  Accept: "application/json",
		  "Content-Type": "application/x-www-form-urlencoded"
		},
		method: "POST"
	})
	.then(response => {
		// if the response is not 200, log an error and return
		if (!response.ok){
			const status = response.status
			const message = response.statusText
			throw {status , message}
		}

		return response.json()
	})
	.then(data => {
		console.log('Success:', data);
		// set api token in local storage
		sessionStorage.setItem("CHATTER_TOKEN", data.access_token)

		// set username in local storage
		sessionStorage.setItem("CHATTER_USERNAME", username)

		// send user to homepage
		window.location.href = "home.html"
		
		//return success message if login takes a bit
		return {status: 200, message : "Success!"}
	})
	.catch((error) => {
		console.error('Error:', error);
		let result = {status : error.status}
		if (error.status == 401){
			result.message = "Incorrect Username or Password"
		} else{
			result.message = "There was an Error. Please try again Later"
		}
		return result
	});
}

loginForm = document.getElementById("login-form")
loginForm.addEventListener("submit", async(e) => {
	e.preventDefault()
	requestBody = {}
	for (element of loginForm.querySelectorAll("input")){
		requestBody[element.id] = element.value
	}
	
	const result = await login(requestBody["username"], requestBody["password"])
	console.log(result)
	const statusMessage = loginForm.querySelector(".status-message")
	statusMessage.innerHTML = result.message
	
	result.status == 200 ? statusMessage.classList.add("success") : statusMessage.classList.add("error")
	
})
