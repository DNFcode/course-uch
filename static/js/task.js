var g={
    editor: undefined,
    files: []
};

var File = function(name, $el, code){
    this.name = name;
    this.$el = $el;
    this.code = code;

    this.set_current = function(){
        g.editor.setValue(this.code);
        this.$el.addClass('current');
    };

    this.save_code = function(){
        this.code = g.editor.getValue();
        this.$el.removeClass('current');
    };

    this.is_current = function(){
        return this.$el.hasClass('current');
    };

    var set_events = function(){
        this.$el.click(function(){
            if(!this.is_current){
                var current = g.files.filter(function(file){
                    return file.is_current();
                })[0];

                current.save_code();
                current.set_current();
            }
        });
    }.bind(this);

    set_events();

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

    $('.file').each(function(){
        var name = $(this).text();
        var code = "";
        g.files.push(new File(name, $(this), code));
    });

    $('.controls .run').click(function(){
        $btn = $(this);
        var data = {};
        g.files.forEach(function(file){
            if (file.is_current()) {
              file.save_code();
              file.set_current();
            }
            data[file.name] = file.code;
        });
        $btn.prop('disabled', true);
        $.ajax({
            url: '/run/',
            method: 'POST',
            data: {files: JSON.stringify(data)},
            success: function(data){
                $('#result').text(data);
                $btn.prop('disabled', false);
            },
            error: function(data){
                $btn.prop('disabled', false);
            }
        })
    });
});
