$(document).ready(function(){

$('.loader').hide()
    var API_KEY = "AIzaSyATVD83kDDkm6eqGY6S-UyMagsZrScjL3E"
    var video = ''
    var videos = $("#videos")

    $("#form").submit(function(event){
        
        event.preventDefault();
        var search = $("#SearchVideo").val()
        
        VideoSearch(API_KEY, search,10)
    })
    function VideoSearch(key , search , max_result){
        videos.empty()
        $.get("https://www.googleapis.com/youtube/v3/search?key="+key+"&type=video&part=snippet&maxResults="+max_result+"&q="+search , function(info){
            console.log(info)
            var x = 1
            info.items.forEach(item => {
                
                video = `<div class="cluster"> <iframe src="https://www.youtube.com/embed/${item.id.videoId}" allowfullscreen value=${x} class="video"> </iframe>
                <p class="titles">${item.snippet.title}</p> </div>`
                videos.append(video)
                x++
            });
            
        })
        
    }

    $('#form1').submit(function(event){
        
        $('#overlay').css("display","block")

    })
    var ex4 = document.getElementById('fcheckbox')
    if (ex4)
    {
    ex4.addEventListener('click',function(){
        var password = document.getElementById('password')
        if(password.type == 'password'){
            password.type = 'text'
        }
        else
        {
            password.type = "password"
        }
    })
}
    var ex =  document.getElementById('scheckbox')
    if (ex)
    {
    ex.addEventListener('click',function(){
        var password = document.getElementById('confirm')
        if(password.type == 'password'){
            password.type = 'text'
        }
        else
        {
            password.type = "password"
        }
    })
}

    var ex1 = document.getElementById('confirm')
    if (ex1)
    {
    ex1.addEventListener('keyup',function(){
        var password = document.getElementById('password')
        var small = document.getElementById('small')
        var button = document.getElementById('register')
        if(password.value == ''){
            small.innerHTML = ''
        }

        else if (password.value != this.value)  
        {
            small.innerHTML = "Passwords don't match!"
            button.disabled = true
        }
        
        else{
            small.innerHTML = ''
            button.disabled = false
        }
    })
}
var ex2 =  document.getElementById('confirmnewpassword')
if (ex2)
{
    ex2.addEventListener('keyup',function(){
        var password = document.getElementById('confirm')
        var small = document.getElementById('small')
        var button = document.getElementById('register')
        if(password.value == ''){
            small.innerHTML = ''
        }

        else if (password.value != this.value)  
        {
            small.innerHTML = "Passwords don't match!"
            button.disabled = true
        }
        
        else{
            small.innerHTML = ''
            button.disabled = false
        }
    })

}
var ex3 = document.getElementById('edit')

if (ex3)
{
    var text = document.getElementById('editname')
    var text1 = document.getElementById('email')
    var newform = document.createElement('form')
    var button1 = document.getElementById('editn')
    var button = document.createElement('button')
    var span = document.getElementById('editaddremove')
    var span1 = document.getElementById('editaddremoveemail')
    var value = text.value
    var value1 = text1.value
    var newinput = document.createElement('input')
    var newinput1 =  document.createElement('input')

    var button2 = document.getElementById('edite')
   
    newform.action = '/account'
    newform.method = 'post'
    newinput.type='text'
    newinput1.type='text'
    newinput.className='infotext'
    newinput1.className='infotext'
    newinput.name = 'name'
    newinput1.name = 'ChangeEmail'

    newinput.placeholder = 'Username'
    newinput1.placeholder = 'Email'
    newinput.value = value
    newinput1.value = value1
    
        
        button1.addEventListener('click',function(event){
        event.preventDefault()
        text.remove()
        button1.remove()
        span.append(newform)
        newform.append(newinput)
        button2.disabled = true
        newform.append(button)
        button.innerHTML = 'save'
        
    })
    newinput.addEventListener('keyup',function(){
        if (newinput.value == ''){
        button.disabled = true
    }
    else{
        button.disabled = false
    }
    })

    button2.addEventListener('click',function(event){
        event.preventDefault()
        text1.remove()
        button2.remove()
        span1.append(newform)
        newform.append(newinput1)
        button1.disabled = true
        newform.append(button)
        button.innerHTML = 'save'
        
    })
    
    newinput1.addEventListener('keyup',function(){
        if (newinput1.value == ''){
        button.disabled = true
    }
    else{
        button.disabled = false
    }
    })
   
}

})
