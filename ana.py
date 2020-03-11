import pandas as pd
import os, sys, json
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm
import requests
myfont = fm.FontProperties(fname='simsun.ttc',size=14)
myfont.set_family('SimHei')

def update_data():
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
    fname = url.split('/')[-1]
    with open(fname, 'w') as f:
        r = requests.get(url)
        req = r.text
        f.write(req)

def ana():
    df0 = pd.read_csv('time_series_19-covid-Confirmed.csv')
    dates = ['%s月%s日' % (v1[0], v1[1]) for v1 in [v.split('/')[:2] for v in df0.columns[4:]]]
    dates = [(df0.columns[4:][i], dates[i]) for i in range(len(dates))]
    df0 = df0.rename(columns=dict(dates))
    df1 = df0.groupby('Country/Region').sum().reset_index()

    top30_cn_str = '中国大陆 意大利 伊朗 韩国 法国 西班牙 美国 德国 钻石公主号邮轮 日本 瑞士 挪威 英国 荷兰 瑞典 \
    比利时 丹麦 奥地利 新加坡 马来西亚 香港特别行政区 巴林王国 澳大利亚 希腊 加拿大 阿联酋 伊拉克 科威特 冰岛 埃及'
    top30_cn = top30_cn_str.split(' ')
    names = ['Mainland China', 'Italy', 'Iran (Islamic Republic of)',
             'Republic of Korea', 'France', 'Spain', 'US', 'Germany', 'Others',
             'Japan', 'Switzerland', 'Norway', 'UK', 'Netherlands', 'Sweden',
             'Belgium', 'Denmark', 'Austria', 'Singapore', 'Malaysia',
             'Hong Kong SAR', 'Bahrain', 'Australia', 'Greece', 'Canada',
             'United Arab Emirates', 'Iraq', 'Kuwait', 'Iceland', 'Egypt']

    top30_cn_dict = dict([(names[i], top30_cn[i]) for i in range(30)])
    df2 = df1.sort_values('3月10日', ascending=False)[:30].reset_index()
    df2['国家/地区'] = top30_cn

    tp = df0.groupby('Province/State').sum().reset_index()
    tp = tp.sort_values('3月10日', ascending=False).reset_index()[:1]
    tp['国家/地区'] = '湖北'
    hubei = tp.values[0][4:-1]
    china = df2[df2['国家/地区'] == '中国大陆'].values[0][4:-1]
    china_nonubei = [china[i] - hubei[i] for i in range(len(china))]


    df = df2

    def draw(ax, v, c, style):
        # ax.plot(range(len(v)), v, label=c )
        ax.semilogy(range(len(v)), v, style, label=c)
        return ax

    plt.rcParams['font.sans-serif'] = ['SimHei']
    fig, ax = plt.subplots(1, 1, figsize=[16, 12])

    counrty_ls = [c for c in top30_cn if c not in ['中国大陆', '钻石公主号邮轮']]
    # counrty_ls = top30_cn

    count = 0
    for c in counrty_ls:
        tp = df[df['国家/地区'] == c]
        v = tp.values[0][4:-1]
        lb = df.columns[4:-1]
        ileft, iright = 0, len(v) - 1
        for i, v1 in enumerate(v):
            ileft = i
            if v1 > 100:
                print(i, c, lb[i], v1)
                break

        for i, v1 in enumerate(v):
            iright = i
            if v1 > 5000:
                break

        print(c, lb[ileft], v[ileft], lb[iright], v[iright])
        v_good = v[ileft:iright + 1]
        v_dif = [0] + [v_good[i + 1] - v_good[i] for i in range(len(v_good) - 1)]
        lc = "%s: %s确诊%s例" % (c, lb[ileft], v_good[0])
        if len(v_good) > 5:
            if count < 9:
                ax = draw(ax, v_good, lc, style='.--')
            else:
                ax = draw(ax, v_good, lc, style='*--')
        count += 1

    # ax = draw(ax, v_sim, '拟合')
    ax = draw(ax, china_nonubei[:25], '中国大陆湖北以外:1月22日确诊103例', style='*--')

    beta = 1.51
    v_sim = [beta ** i * 100 for i in range(13)]
    func = '$f(t)=%s^t * 100$' % (str(beta))
    ax.semilogy(range(len(v_sim)), v_sim, 'rs-', label='指数拟合1: %s' % (func))
    plt.text(len(v_sim) - 1, v_sim[-1], func, fontsize=16)

    beta = 1.11
    v_sim = [beta ** i * 100 for i in range(20)]
    func = '$f(t)=%s^t * 100$' % (str(beta))
    ax.semilogy(range(len(v_sim)), v_sim, 'gs-', label='指数拟合2: %s' % (func))
    plt.text(len(v_sim) - 6, v_sim[-1], func, fontsize=16)
    beta = 1.03
    v_sim = [beta ** i * 100 for i in range(20)]
    func = '$f(t)=%s^t * 100$' % (str(beta))
    ax.semilogy(range(len(v_sim)), v_sim, 'bs-', label='指数拟合3: %s' % (func))
    plt.text(len(v_sim) - 6, v_sim[-1], func, fontsize=16)

    plt.yticks([100, 200, 500, 1000, 2000, 5000, 10000, 20000], [100, 200, 500, 1000, 2000, 5000, 10000, 20000],
               fontsize=14)
    plt.ylim([0, 20000])
    plt.ylabel('确诊人数', fontproperties=myfont, fontsize=18)
    # lb = df.columns[20:]
    # ax = draw(ax, hubei, '湖北', style='*-')
    # plt.text(-2,2,r'sf',fontsize=16)

    lb = ['%d天后' % (i) if i % 5 == 0 else '' for i in range(30)]
    lb[0] = '起始日'
    _ = plt.xticks(range(len(lb)), lb, rotation=30, fontproperties=myfont, fontsize=16)
    plt.legend(prop=myfont, fontsize=30, loc=0)
    plt.title("4.各国家/地区确诊病例突破100人后的时序增长图-对数拟合", fontproperties=myfont, fontsize=22)
    plt.savefig('4各国家地区确诊病例突破100人后的时序增长图-对数拟合.png')

if __name__ == '__main__':
    #update_data()
    ana()

