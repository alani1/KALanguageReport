;(function($){
ListFilterCollapsePrototype = {
    bindToggle: function(){
        var that = this;
        this.$filterEl.click(function(){
            that.$filterList.slideToggle();
        });
    },
    init: function(filterEl) {
        this.$filterEl = $(filterEl).css('cursor', 'pointer');
        this.$filterList = this.$filterEl.next('ul').hide();
        this.bindToggle();
    }
}
function ListFilterCollapse(filterEl) {
    this.init(filterEl);
}
ListFilterCollapse.prototype = ListFilterCollapsePrototype;


function selectFilter(select,value) {

    var newURL = window.location.protocol + "//" + window.location.host + "/" + window.location.pathname;

    document.location = newURL + value;
}

$.fn.selectFilterOptions = function () {

    alert(this);
}

$(document).ready(function(){

    //First check URL and select the options
    //$('select').selectFilterOptions();
    
    $('div#changelist-filter select').multipleSelect({filter: true, selectAll: false,single: true,
    
    onClick: function(view) {
       selectFilter( view.checked, view.value);
    }
    
    });

    $('#changelist-filter').children('h3').each(function(){
        var collapser = new ListFilterCollapse(this);
    });
});

})(django.jQuery);
