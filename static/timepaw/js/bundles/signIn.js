m.utilities={breakURLCache:function(a){return a+"?breakCache="+(new Date).getTime()},browser:{init:function(){this.browser=this.searchString(this.dataBrowser)||"An unknown browser";this.version=this.searchVersion(navigator.userAgent)||this.searchVersion(navigator.appVersion)||"an unknown version";this.OS=this.searchString(this.dataOS)||"an unknown OS"},searchString:function(a){for(var b=0;b<a.length;b++){var e=a[b].string,c=a[b].prop;this.versionSearchString=a[b].versionSearch||a[b].identity;if(e){if(e.indexOf(a[b].subString)!=
-1)return a[b].identity}else if(c)return a[b].identity}},searchVersion:function(a){var b=a.indexOf(this.versionSearchString);return b==-1?void 0:parseFloat(a.substring(b+this.versionSearchString.length+1))},dataBrowser:[{string:navigator.userAgent,subString:"Chrome",identity:"Chrome"},{string:navigator.userAgent,subString:"OmniWeb",versionSearch:"OmniWeb/",identity:"OmniWeb"},{string:navigator.vendor,subString:"Apple",identity:"Safari",versionSearch:"Version"},{prop:window.opera,identity:"Opera"},
{string:navigator.vendor,subString:"iCab",identity:"iCab"},{string:navigator.vendor,subString:"KDE",identity:"Konqueror"},{string:navigator.userAgent,subString:"Firefox",identity:"Firefox"},{string:navigator.vendor,subString:"Camino",identity:"Camino"},{string:navigator.userAgent,subString:"Netscape",identity:"Netscape"},{string:navigator.userAgent,subString:"MSIE",identity:"Explorer",versionSearch:"MSIE"},{string:navigator.userAgent,subString:"Gecko",identity:"Mozilla",versionSearch:"rv"},{string:navigator.userAgent,
subString:"Mozilla",identity:"Netscape",versionSearch:"Mozilla"}],dataOS:[{string:navigator.platform,subString:"Win",identity:"Windows"},{string:navigator.platform,subString:"Mac",identity:"Mac"},{string:navigator.userAgent,subString:"iPhone",identity:"iPhone/iPod"},{string:navigator.platform,subString:"Linux",identity:"Linux"}]},capitalizeString:function(a){return a.charAt(0).toUpperCase()+a.slice(1)},wait:function(a){return $.Deferred(function(b){setTimeout(b.resolve,a)})},dateFormatRelative:function(a){var a=
new Date(a*1E3),b=new Date,e="",e=(b.getTime()-a.getTime())/6E4,c=b.getHours()*60+b.getMinutes();return e=a.getYear()<b.getYear()?this.dateFormat(a,"mmm d, yyyy",false):e-c>1440?this.dateFormat(a,"mmm d",false):e-c>0?"yesterday":e<60?Math.floor(e)+" min ago":Math.floor(e/60)+" hrs ago"},cleanMemoId:function(a){return a.replace(/[:=-_@\.\/]/g,"")},dateFormat:function(){var a=/d{1,4}|m{1,4}|yy(?:yy)?|([HhMsTt])\1?|[LloSZ]|"[^"]*"|'[^']*'/g,b=/\b(?:[PMCEA][SDP]T|(?:Pacific|Mountain|Central|Eastern|Atlantic) (?:Standard|Daylight|Prevailing) Time|(?:GMT|UTC)(?:[-+]\d{4})?)\b/g,
e=/[^-+\dA-Z]/g,c=function(a,b){a=String(a);for(b=b||2;a.length<b;)a="0"+a;return a};return function(d,h,j){var l,n,g;g={"default":"ddd mmm dd yyyy HH:MM:ss",shortDate:"m/d/yy",shortDateWithZero:"mm/dd/yyyy",mediumDate:"mmm d, yyyy",longDate:"mmmm d, yyyy",fullDate:"dddd, mmmm d, yyyy",fullDatePlusTime:"dddd, mmmm d - h:MM tt",fullDateAndTime:"m/d/yy h:MM:ss TT Z",shortTime:"h:MM TT",mediumTime:"h:MM:ss TT",longTime:"h:MM:ss TT Z",isoDate:"yyyy-mm-dd",isoTime:"HH:MM:ss",isoDateTime:"yyyy-mm-dd'T'HH:MM:ss",
isoUtcDateTime:"UTC:yyyy-mm-dd'T'HH:MM:ss'Z'"};l="Sun,Mon,Tue,Wed,Thu,Fri,Sat,Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday".split(",");n="Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec,January,February,March,April,May,June,July,August,September,October,November,December".split(",");arguments.length==1&&Object.prototype.toString.call(d)=="[object String]"&&!/\d/.test(d)&&(h=d,d=void 0);d=d?new Date(d):new Date;if(isNaN(d))throw SyntaxError("invalid date");h=String(g[h]||h||g["default"]);
h.slice(0,4)=="UTC:"&&(h=h.slice(4),j=true);var f=j?"getUTC":"get";g=d[f+"Date"]();var p=d[f+"Day"](),k=d[f+"Month"](),q=d[f+"FullYear"](),i=d[f+"Hours"](),r=d[f+"Minutes"](),s=d[f+"Seconds"](),f=d[f+"Milliseconds"](),o=j?0:d.getTimezoneOffset(),t={d:g,dd:c(g),ddd:l[p],dddd:l[p+7],m:k+1,mm:c(k+1),mmm:n[k],mmmm:n[k+12],yy:String(q).slice(2),yyyy:q,h:i%12||12,hh:c(i%12||12),H:i,HH:c(i),M:r,MM:c(r),s:s,ss:c(s),l:c(f,3),L:c(f>99?Math.round(f/10):f),t:i<12?"a":"p",tt:i<12?"am":"pm",T:i<12?"A":"P",TT:i<
12?"AM":"PM",Z:j?"UTC":(String(d).match(b)||[""]).pop().replace(e,""),o:(o>0?"-":"+")+c(Math.floor(Math.abs(o)/60)*100+Math.abs(o)%60,4),S:["th","st","nd","rd"][g%10>3?0:(g%100-g%10!=10)*g%10]};return h.replace(a,function(a){return a in t?t[a]:a.slice(1,a.length-1)})}}(),convertURLstringsToAnchors:function(a){return a.replace(/[A-Za-z]+:\/\/[A-Za-z0-9-_]+\.[A-Za-z0-9-_:%&~\?\/.=]+/g,function(a){return a.link(a)})},urlHash:{set:function(a){var a=$.toQueryParams(a),b=$.toQueryParams(location.hash),
e;for(e in a)b[e]=a[e];return $.toQueryString(b)},remove:function(a){var a=$.toQueryParams(a),b=$.toQueryParams(location.hash),e={},c;for(c in b)a[c]==void 0&&(e[c]=b[c]);return $.toQueryString(e)},get:function(a){return typeof a=="undefined"?$.toQueryParams(location.hash):$.toQueryParams(location.hash)[a]},go:function(a){location.hash=a.substr(0,1)=="#"?a:"#"+a;return false}}};
m.globalTemplates={dialogs:{removeLane:'<div id="" class="memolaneDialog">\t<div class="dialogTopBar">\t\t<div class="dialogTitle">Remove Lane</div>\t\t<div class="close closeMemolaneDialog cancelAddingBtn">cancel</div>\t\t<div class="clearFloatNoHeight"></div>\t</div>\t<div class="dialogContent">\t\t<p><strong>Are you sure you want to remove <strong>${title}</strong> from Memolane?</strong></p>\t\t<p>All settings will be lost, and any work you\'ve put into curating this lane will be permanently gone!</p>\t\t<p><a href="#" class="btn-red float-left removeConfirm close">Yes, REMOVE the lane!</a> <a href="#" class="secondaryAction float-left close">No, I don\'t want that</a></p>\t</div></div>',removeLaneContributor:'<div id="" class="memolaneDialog">\t<div class="dialogTopBar">\t\t<div class="dialogTitle">Stop Contributing?</div>\t\t<div class="close closeMemolaneDialog cancelAddingBtn">cancel</div>\t\t<div class="clearFloatNoHeight"></div>\t</div>\t<div class="dialogContent">\t\t<p><strong>Are you sure you wish to stop contributing to this lane: ${lane_title}</strong></p>\t\t<p><a href="#" class="btn-red float-left removeConfirm close">Remove me as a contributor from this lane</a> <a href="#" class="secondaryAction float-left close">No, I don\'t want that</a></p>\t</div></div>',
addFriend:'<div id="" class="memolaneDialog">\t<div class="dialogTopBar">\t\t<div class="dialogTitle">Friend Request Sent</div>\t\t<div class="close closeMemolaneDialog cancelAddingBtn">close</div>\t\t<div class="clearFloatNoHeight"></div>\t</div>\t<div class="dialogContent">\t\t<h2 class="header typeJ">Cross your fingers!</h2>\t\t<p>You just sent a friend request to <strong>${first_name} ${last_name}</strong>.</p>\t\t<p><a href="#" class="btn-green float-left close">OK</a></p>\t</div></div>',acceptFriendRequest:'<div id="" class="memolaneDialog">\t<div class="dialogTopBar">\t\t<div class="dialogTitle">Accepted Friend Request</div>\t\t<div class="close closeMemolaneDialog cancelAddingBtn">close</div>\t\t<div class="clearFloatNoHeight"></div>\t</div>\t<div class="dialogContent">\t\t<h2 class="header typeJ">We\'re friends!</h2>\t\t<p>You just accepted <strong>${first_name} ${last_name}\'s</strong> friend request!</p>\t\t<p>You can now see each other\'s "Friends Only" memos.</p>\t\t<p><a href="#" class="btn-green float-left close">OK</a></p>\t</div></div>',
rejectFriendRequest:'<div id="" class="memolaneDialog">\t<div class="dialogTopBar">\t\t<div class="dialogTitle">Rejected Friend Request</div>\t\t<div class="close closeMemolaneDialog cancelAddingBtn">close</div>\t\t<div class="clearFloatNoHeight"></div>\t</div>\t<div class="dialogContent">\t\t<h2 class="header typeJ">It\'s not you, it\'s me</h2>\t\t<p>You just rejected <strong>${first_name} ${last_name}\'s</strong> friend request.</p>\t\t<p>At this point, you can only see each other\'s public memos.</p>\t</div></div>',
cancelFriendRequest:'<div id="" class="memolaneDialog">\t<div class="dialogTopBar">\t\t<div class="dialogTitle">Cancelled Friend Request</div>\t\t<div class="close closeMemolaneDialog cancelAddingBtn">close</div>\t\t<div class="clearFloatNoHeight"></div>\t</div>\t<div class="dialogContent">\t\t<h2 class="header typeJ">It\'s not you, it\'s me</h2>\t\t<p>You just cancelled your request for <strong>${first_name} ${last_name}\'s</strong> friendship.</p>\t\t<p>At this point, you can only see each other\'s public memos.</p>\t</div></div>',
removeFriend:'<div id="" class="memolaneDialog">\t<div class="dialogTopBar">\t\t<div class="dialogTitle">Remove Friend?</div>\t\t<div class="close closeMemolaneDialog cancelAddingBtn">cancel</div>\t\t<div class="clearFloatNoHeight"></div>\t</div>\t<div class="dialogContent">\t\t<p><strong>Are you sure you want to cancel your Memolane friendship with ${first_name} ${last_name}</strong>?</p>\t\t<p>You and ${first_name} ${last_name} will lose the ability to see each other\'s "Friends Only" memos and contribute to each other\'s lanes.</p>\t\t<p><a href="#" class="btn-red float-left removeConfirm close">Yes, REMOVE the friend!</a> <a href="#" class="secondaryAction float-left close">No, I don\'t want that</a></p>\t</div></div>'}};
m.deviceIsIpad=navigator.userAgent.match(/iPad/i)!=null;m.deviceIsIphone=navigator.userAgent.match(/iPhone/i)!=null;m.deviceIsAndroid=navigator.userAgent.toLowerCase().indexOf("android")>-1;m.isIE9=$.browser.version==="9.0"?true:false;m.isIE8=$.browser.version==="8.0"?true:false;m.clickOrTouchStart=Modernizr.touch?"touchstart":"click";m.clickOrTouchEnd=Modernizr.touch?"touchend":"click";m.mouseEnterOrTouchStart=Modernizr.touch?"touchstart":"mouseenter";
m.mouseLeaveOrTouchEnd=Modernizr.touch?"touchend":"mouseleave";m.mouseDownOrTouchStart=Modernizr.touch?"touchstart":"mousedown";m.mouseMoveOrTouchMove=Modernizr.touch?"touchmove":"mousemove";m.mouseUpOrTouchEnd=Modernizr.touch?"touchend":"mouseup";m.mouseOutOrTouchEnd=Modernizr.touch?"touchend":"mouseout";m.mouseOverOrTouchStart=Modernizr.touch?"touchstart":"mouseover";
m.topBar=function(a,b){return{initialize:function(){b(a).bind("resize",function(){m.topBar.runLayout()});this.runLayout()},runLayout:function(){var a=b("body"),c=b("#header"),d=b("#tb-search input");a.width()<1E3&&(c.removeClass("more1024").addClass("less1024"),d.attr("value","Search"));a.width()>=1E3&&(c.removeClass("less1024").addClass("more1024"),m.currentLane?d.attr("value","Search memos, lanes & users"):d.attr("value","Search lanes & users"))}}}(this,jQuery,this.undefined);m.topBar.initialize();
m.signin=function(a,b){return{$passwordInput:b("#password"),$usernameInput:b("#username"),$rememberOption:b("#remember"),$usernameInputAndpasswordInput:b("#username,#password"),$signinForm:b("#signin"),initialize:function(){this.maskInputs();b.validity.setup({outputMode:"modal"});this.$signinForm.submit(b.proxy(function(){this.loginIn();return false},this))},loginIn:function(){var a=this;this.validateForm()&&(b(".form-message-error").hide(),b.ajax({type:"POST",url:"/login",data:{password:this.$passwordInput.val(),
username:this.$usernameInput.val(),remember:this.$rememberOption.val()},error:function(){a.$signinForm.find(".form-message-error").show().end().find("#password").val("");a.$signinForm.find("input[type=text]").keyup(function(){a.$signinForm.find(".form-message-error").fadeOut()})},success:function(){window.location.href="/me"}}))},validateForm:function(){b.validity.start();b("#password").require();b("#username").require().filter(function(){return b(this).val().match(/@/g)}).match("email","Please enter a valid email!");
return b.validity.end().valid},maskInputs:function(){this.$usernameInput.keypress(function(a){a.which==32&&a.preventDefault()})}}}(this,jQuery,this.undefined);m.signin.initialize();m.currentUser?$(".user-is-logged-in").show():$(".user-is-not-logged-in").show();$.fn.lightbox_me.defaults.destroyOnClose=true;$.fn.lightbox_me.defaults.centered=true;m.utilities.browser.init();var currentBrowser=m.utilities.browser;
(currentBrowser.browser==="Firefox"&&parseInt($.browser.version,10)<6||currentBrowser.browser==="Opera"&&parseInt($.browser.version,10)<11||currentBrowser.browser==="Explorer"&&parseInt($.browser.version,10)<9)&&$('<div class="notifications badnews-notice"><div class="notice-text">请考虑升级您的浏览器，我们建议使用Explorer 9, Opera 11+, Chrome 12+, Firefox 6+, and Safari 5+浏览TimePaw，暂不支持手机客户端！<a href="#" class="close-notice">X</a></div></div>').notify({expires:false});$.ajaxSetup({data:{_csrf:m.csrf}});
$.ajaxPrefilter(function(a){a.type.toLowerCase()==="delete"&&(a.data+="&_method=DELETE")});
