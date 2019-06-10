var currentCid = 1; // 当前分类 id
var cur_page = 1; // 当前页
var total_page = 1;  // 总页数
var data_querying = true;   // 是否正在向后台获取数据


$(function () {
    // 当我们进入首页的时候，要加载新闻数据
    updateNewsData()
    // 首页分类切换
    $('.menu li').click(function () {
        var clickCid = $(this).attr('data-cid')
        $('.menu li').each(function () {
            $(this).removeClass('active')
        })
        $(this).addClass('active')

        if (clickCid != currentCid) {
            // 记录当前分类id
            currentCid = clickCid

            // 重置分页参数
            cur_page = 1
            total_page = 1
            updateNewsData()
        }
    })

    //页面滚动加载相关
    $(window).scroll(function () {

        // 浏览器窗口高度
        var showHeight = $(window).height();

        // 整个网页的高度
        var pageHeight = $(document).height();

        // 页面可以滚动的距离
        var canScrollHeight = pageHeight - showHeight;

        // 页面滚动了多少,这个是随着页面滚动实时变化的
        var nowScroll = $(document).scrollTop();

        if ((canScrollHeight - nowScroll) < 100) {
            // 判断页数，去更新新闻数据
            // 加载更多数据是有条件的
            // 1.比如说已经到最后一页了，不在加载
            // 2.如果正在加载数据，不在加载
            if (!data_querying){
                // false 代表不加载数据，true加载数据
                // 如果data_querying = false 我加载数据
                if (cur_page < total_page){
                    data_querying = true
                    cur_page += 1
                    updateNewsData()
                }
            }else {
                data_querying = false
            }
        }
    })
})

function updateNewsData() {
    // 更新新闻数据
    var params = {
        "cid": currentCid,
        "page":cur_page
    }
    $.get("/news_list",params,function (response) {
        if (response.errno == "0") {
            // 在第一次加载的时候，就因该修改他的总页数
            total_page = response.data.total_page
            // 成功加载数据
            data_querying = false
            //显示数据
            // 清空原有数据
            // 只有当前页为第一页的时候才清楚说有的数据，第二页不需要清楚
            if (cur_page == 1){
            $(".list_con").html("")}
            for (var i = 0; i < response.data.news_dict_li.length; i++) {
                var news = response.data.news_dict_li[i]
                var content = '<li>'
                content += '<a href="#" class="news_pic fl"><img src="' + news.index_image_url + '?imageView2/1/w/170/h/170"></a>'
                content += '<a href="#" class="news_title fl">' + news.title + '</a>'
                content += '<a href="#" class="news_detail fl">' + news.digest + '</a>'
                content += '<div class="author_info fl">'
                content += '<div class="source fl">来源：' + news.source + '</div>'
                content += '<div class="time fl">' + news.create_time + '</div>'
                content += '</div>'
                content += '</li>'
                $(".list_con").append(content)
            }
        } else {
            alert(reponse.errmsg)
        }

    })

}

