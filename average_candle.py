from time import sleep
import threading
'''
10초 단위로 현재가를 얻어온다.
그래서 10초단위의 10평선, 15평선 두개를 기준으로
10평선이 15평선을 넘어섰을경우 시장가로 구매
10평선이 15평선 아래로 내려갈 경우 시장가로 매도

'''

class AvgCandle():
    TICK_WAITTIME = 0.1
    START_MONEY = 10000
    WAITTIME= 10

    def __init__(self, trader):
        print('AvgCandle initiate')
        self.trader = trader
        self.seedMoney = AvgCandle.START_MONEY
        self.tickPriList = [0]*15
        self.doBuy = 0
        self.isCoin = False
        self.haveCoin = 0
        self.judge = 0
        self.lastuuid = 0

    def start(self):
        self.selectedCoin = self.SelectCoin()
        print('selected coin is {}'.format(self.selectedCoin))

        #15틱을 저장하기 위해 총 WAITTIME*15초 동안 저장
        for i in range(14,-1,-1):
            self.tickPriList[i] = self.trader.getCurrentPrice(self.selectedCoin)
            sleep(AvgCandle.WAITTIME)
            print(self.tickPriList[i])
        self.newTick = 0

        #Thread로 코인가격 받아오기.
        self.conGetPrice = threading.Timer(AvgCandle.WAITTIME, self.GetPrice)
        self.conGetPrice.start()
        while 1:
            # 매수 매도 포지션이 바뀌었을경우에는 어떤 경우에서든 주문을 취소한다.
            if self.judge == 0:
                pass
            elif self.doBuy != self.judge:
                self.CancelOrder()
                self.doBuy = self.judge

            #1. 그래프보다 낮을경우 사라. 높을경우 팔아라.
            #2. 지정가 매수를 했다. 이때 (1) 아예 안사진경우 (2) 일부만 사진경우 (3) 다 사진경우
            #3. 지정가 매도를 했다. 이때 (1) 아예 안팔린경우 (2) 일부만 팔린경우 (3) 다 팔린경우
            if self.doBuy == 1 and self.newTick == 1:
                self.newTick = 0
                self.BuyCoin()
            elif self.doBuy == -1 and self.newTick == 1:
                self.newTick = 0
                self.SellCoin()
            sleep(AvgCandle.TICK_WAITTIME)
    def SelectCoin(self):
        stockList = self.trader.getStocksList()
        maxVolume = 0
        selectedCoin = ''
        for i in stockList:
            result = self.trader.getDayCandle(i)
            if maxVolume < result['candle_acc_trade_price']:
                maxVolume = result['candle_acc_trade_price']
                selectedCoin = i
            sleep(0.1)
        return selectedCoin

    def JudgeGraph(self):
        '''
        
        :return: 1은 10틱이 아래일때, -1은 10틱이 위에일때, 0은 같을떄.
        '''
        tenAvg = int(sum(self.tickPriList[5:]) / 10)
        fifteenAvg = int(sum(self.tickPriList) / 15)
        print('tenAvg is {}'.format(tenAvg))
        print('fifteenAvg is {}'.format(fifteenAvg))
        if tenAvg < fifteenAvg :
            self.judge = 1
        elif tenAvg > fifteenAvg :
            self.judge = -1
        else :
            self.judge = 0

    def GetPrice(self):
        # 코인 동기화
        self.tickPriList.pop(0)
        self.tickPriList.append(self.trader.getCurrentPrice(self.selectedCoin))
        self.JudgeGraph()
        self.newTick = 1
        threading.Timer(AvgCandle.WAITTIME, self.GetPrice).start()


    def BuyCoin(self):
        balance = self.trader.getBalance()
        money = 0
        for i in balance:
            if 'KRW' == i['currency']:
                money = i['balance']
                money = int(float(money))
                break
        price = self.trader.getCurrentPrice(self.selectedCoin)
        amount = int(money/price)
        result = self.trader.sendBuying(self.selectedCoin, amount, '지정가', price)
        try:
            self.lastuuid = result[0]['uuid']
        except:
            print('is in BuyCoin')
            pass

    def SellCoin(self):
        price = self.trader.getCurrentPrice(self.selectedCoin)
        #지금 가지고있는 코인 개수 확인해야함
        amount = self.trader.getBalance()
        for i in amount:
            if self.selectedCoin[4:] == i['currency']:
                amount = i['balance']
                amount = int(float(amount))
                break
        result = self.trader.sendSelling(self.selectedCoin, amount, '지정가', price)
        try:
            self.lastuuid = result[0]['uuid']
        except:
            print('is in SellCoin')
            pass


    def checkBuy(self):
        pass

    def checkSell(self):
        pass

    def checkBalance(self):
        pass

    def CancelOrder(self):
        self.trader.CancelOrder(self.lastuuid)
        pass







if __name__ == '__main__':
    print('average algorithm')