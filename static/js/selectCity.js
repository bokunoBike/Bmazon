//****************所使用的数据是city.js******************//
/*根据id获取对象*/
function $(str) {
    return document.getElementById(str);
}

var titleWrap = $('title-wrap').getElementsByTagName('li');
var addrWrap = $('addr-wrap');   //省市区显示模块
var address_province = $('id_address_province');
var address_city = $('id_address_city');
var address_town = $('id_address_town');

var current2 = {
    prov: '',
    city: '',
    country: '',
    provVal: '',
    cityVal: '',
    countryVal: ''
};

/*自动加载省份列表*/
window.onload = showProv2();

function showProv2() {
    addrWrap.innerHTML = '';
    titleWrap[0].className = 'titleSel';
    var len = provice.length;
    for (var i = 0; i < len; i++) {
        var provLi = document.createElement('li');
        provLi.innerText = provice[i]['name'];
        provLi.index = i;
        addrWrap.appendChild(provLi);
    }
}

/*************************需要给动态生成的li绑定点击事件********************** */
addrWrap.onclick = function (e) {
    var n;
    var e = e || window.event;
    var target = e.target || e.srcElement;
    if (target && target.nodeName == 'LI') {
        /*先判断当前显示区域显示的是省市区的那部分*/
        for (var z = 0; z < 3; z++) {
            if (titleWrap[z].className == 'titleSel')
                n = z;
        }
        /*显示的处理函数*/
        switch (n) {
            case 0:
                showCity2(target.index);
                break;
            case 1:
                showCountry2(target.index);
                break;
            case 2:
                selectCountry(target.index);
                break;
            default:
                showProv2();
        }
    }
};

/*选择省份之后显示该省下所有城市*/
function showCity2(index) {
    addrWrap.innerHTML = '';
    current2.prov = index;
    current2.provVal = provice[index].name;
    titleWrap[0].className = '';
    titleWrap[1].className = 'titleSel';
    var cityLen = provice[index].city.length;
    for (var j = 0; j < cityLen; j++) {
        var cityLi = document.createElement('li');
        cityLi.innerText = provice[index].city[j].name;
        cityLi.index = j;
        addrWrap.appendChild(cityLi);
    }
    //将选中的省份填到输入框中
    address_province.value = current2.provVal;
}

/*选择城市之后显示该城市下所有县区*/
function showCountry2(index) {
    addrWrap.innerHTML = '';
    current2.city = index;
    current2.cityVal = provice[current2.prov].city[index].name;
    titleWrap[1].className = '';
    titleWrap[2].className = 'titleSel';
    var countryLen = provice[current2.prov].city[index].districtAndCounty.length;
    if (countryLen == 0) {
        address_province.value = current2.provVal;
        address_city.value = '-';
        address_town.value = current2.countryVal;
    }
    for (var k = 0; k < countryLen; k++) {
        var cityLi = document.createElement('li');
        cityLi.innerText = provice[current2.prov].city[index].districtAndCounty[k];
        cityLi.index = k;
        addrWrap.appendChild(cityLi);
    }
    //将选中的城市填到输入框中
    address_city.value = current2.cityVal;
}

/*选中具体的县区*/
function selectCountry(index) {
    current2.country = index;
    // addrWrap.getElementsByTagName('li')[index].style.backgroundColor = '#23B7E5';
    current2.countryVal = provice[current2.prov].city[current2.city].districtAndCounty[index];
    //将选中的县区填到输入框中
    address_town.value = current2.countryVal;
}


/*分别点击省市区标题的处理函数*/
document.getElementById('title-wrap').onclick = function (e) {
    var e = e || window.event;
    var target = e.target || e.srcElement;
    if (target && target.nodeName == 'LI') {
        for (var z = 0; z < 3; z++) {
            titleWrap[z].className = '';
        }
        target.className = 'titleSel';
        if (target.value == '0') {
            showProv2();
        } else if (target.value == '1') {
            showCity2(current2.prov);
        } else {
            showCountry2(current2.city);
        }
    }
};