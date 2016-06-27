/**
 *
 * @authors moling (365024424@qq.com)
 * @date    2016-06-26 21:07:03
 * @version $Id$
 */
var table = location.pathname.split('/').pop();

function getItemsByPage(page, size='10') {
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
                    if (err) {
                        return alert(err.message || err.error || err);
                    }
                    if (vm.items.length > 10) {
                        vm.items.$remove(item);
                    }
                    else{
                        getItemsByPage(vm.page.page_index, vm.page.page_size);
                    }
                });
            }
        },
        gotoPage: function (page) {
            return getItemsByPage(page, vm.page.page_size);
        }
    }
});

$(function() {
    getItemsByPage(getUrlParams('page'), getUrlParams('size'));
});
