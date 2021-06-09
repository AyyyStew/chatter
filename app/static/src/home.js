// check if a token exists in session storage.
// if it doens't send user back to the login screen 
const redirectIfNoToken = ()=>{
	const token = sessionStorage.getItem("CHATTER_TOKEN")

	if (token === null){
		window.location.replace("index.html")
	}
}
redirectIfNoToken()