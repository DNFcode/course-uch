var g={
    editor: undefined,
    files: undefined
};

var File = function(name, $el, code){
    this.name = name;
    this.$el = $el;
    this.code = code;
    
    this.$el.bind('change_file', $.proxy(function(){
        this.code = g.editor.getValue();
        this.$el.removeClass('current');
    }, this));
    
    this.$el.bind('set_current', $.proxy(function(){
        if (!this.is_current()){
            g.editor.setValue(this.code);
            this.$el.addClass('current');
        }
    }, this));
    
    var is_current = function(){
        return this.$el.hasClass('current');
    }.bind(this);
    
}

$(document).ready(function(){
    g.editor = ace.edit("editor");
    g.editor.setTheme("ace/theme/chrome");
    g.editor.getSession().setMode("ace/mode/rust");
    
    $('.header-right .menu').click(function(){
        $('.tasks-nav').animate({width:"toggle"}, 350);
    });
    
    $('.tasks-nav .back').click(function(){
        $('.tasks-nav').animate({width:"toggle"}, 350);
    });
})