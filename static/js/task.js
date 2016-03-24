$(document).ready(function(){
    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/chrome");
    editor.getSession().setMode("ace/mode/rust");
    
    $('.header-right .menu').click(function(){
        $('.tasks-nav').animate({width:"toggle"}, 350);
    });
    
    $('.tasks-nav .back').click(function(){
        $('.tasks-nav').animate({width:"toggle"}, 350);
    });
})