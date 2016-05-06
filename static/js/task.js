var g={
    editor: undefined,
    files: [],
    current_file: undefined,
    last_current_file: undefined
};

var File = function(name, $el, code, is_tab){
    this.name = name;
    this.$el = $el;
    this.code = code;
    this.is_tab = is_tab;

    this.set_current = function(){
        g.editor.setValue(this.code);
        this.$el.addClass('current');
        g.current_file = this;
    };

    this.save_code = function(){
        this.code = g.editor.getValue();
        this.$el.removeClass('current');
    };

    this.is_current = function(){
        return this.$el.hasClass('current');
    };

    var set_events = function(){
        var self = this;
        this.$el.click(function(){
            if(!self.is_current()){
                g.current_file.save_code();
                if(!self.is_tab){
                    $('.current-file').text(self.$el.text());
                    g.last_current_file = self;
                    $('.current-file').addClass('active');
                    $('.input').removeClass('active');
                }

                self.set_current();
            }
        });
    }.bind(this);

    set_events();

};

function setup_ace(){
    g.editor = ace.edit("editor");
    g.editor.setTheme("ace/theme/chrome");
    g.editor.getSession().setMode("ace/mode/rust");
}

function setup_burger(){
    $('.header-right .menu').click(function(){
        $('.tasks-nav').animate({width:"toggle"}, 350);
    });

    $('.tasks-nav .back').click(function(){
        $('.tasks-nav').animate({width:"toggle"}, 350);
    });
}

function setup_files(){
    $('.file').each(function(){
        var name = $(this).text();
        if ($(this).parent().hasClass('folder') && !$(this).parent().hasClass('files')){
            var folder_name = $(this).parent().find('.folder-name').text();
            name = folder_name + '/' + name;
        }
        var code = "";
        g.files.push(new File(name, $(this), code));
        if (g.files[g.files.length-1].is_current()){
            g.current_file = g.files[g.files.length-1];
            g.last_current_file = g.files[g.files.length-1];
        }
    });

    g.files.push(new File('input', $('.code-editor .input'), "", true));

    $('.current-file').text($('.file.current').text());

    $('.current-file').click(function(){
        g.current_file.save_code();
        g.last_current_file.set_current();
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
                data = data.replace(/\n/g, '<br>');
                data = data.replace(/ /g, '&nbsp;');
                $('#result').html(data);
                $btn.prop('disabled', false);
            },
            error: function(data){
                $btn.prop('disabled', false);
            }
        })
    });
}

function setup_tabs(){
    $('.tabs').on('click', '.tab:not(.active)', function(){
        $(this).parent().find('.active').removeClass('active');
        $(this).addClass('active');
        if($(this).attr('data-tab-id')) {
            $('.tab-content.active').removeClass('active');
            var id = $(this).attr('data-tab-id');
            $('.tab-content[data-tab-id=' + id + ']').addClass('active');
        }
    })
}

$(document).ready(function(){
    setup_ace();
    setup_burger();
    setup_files();
    setup_tabs();
});
