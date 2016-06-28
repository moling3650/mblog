/**
 *
 * @authors moling (365024424@qq.com)
 * @date    2016-06-26 21:07:03
 * @version $Id$
 */
var table = location.pathname.split('/').pop();

function getItemsByPage (page, size) {
    $.getJSON('/api/' + table, {
        page: page || '1',
        size: size || '10'
    }, function (data) {
        vm.items = data.items;
        vm.page = data.page;
    });
}

var vm = new Vue({
    el: '#vm',
    data: {
        items: [],
        page: null,
        models: {
            'users': {'name': '名字', 'email': '电子邮箱'},
            'blogs': {'name': '标题', 'user_name': '作者'},
            'comments': {'user_name': '作者', 'content':'内容'}
        },
    },
    computed:{
        fields: function () {
            return this.models[table];
        }
    },
    methods: {
        delete_item: function (item) {
            if (confirm('确认要删除“' + (item.name || item.content) + '”？删除后不可恢复！')) {
                postJSON('/api/' + table + '/' + item.id + '/delete', function (err, r) {
                    if (this.items.length > 10) {
                        this.items.$remove(item);
                    }
                    else{
                        getItemsByPage(this.page.index, this.page.limit);
                    }
                });
            }
        },
        vaildPage: function(i) {
            return (i > 1) && (Math.abs(i - this.page.index) < 3);
        },
        gotoPage: function (page) {
            return getItemsByPage(page, this.page.limit);
        }
    }
});

$(function() {
    getItemsByPage(getUrlParams('page'), getUrlParams('size'));
});
