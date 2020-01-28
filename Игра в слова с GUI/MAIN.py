# (c) Masahiko AMANO (H1K0)
#from os import access, F_OK, mkdir, rename
#from shutil import copyfile
from PyQt5 import uic
from PyQt5.QtWidgets import (
    QApplication, QMainWindow,
    QWidget, QDialog,
    QFileDialog, QInputDialog
)
#from PyQt5.QtGui import QPixmap
from wordwork import *
#from logwork import Log
#from click import clickable
import client


class Start(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('start.ui',self)
        self.game_ai.clicked.connect(self.play_with_ai)
        self.game_create.clicked.connect(self.create)
        self.game_join.clicked.connect(self.join)

    def play_with_ai(self):
        global choose,opponent
        opponent='AI'
        choose=Choose('AI')
        choose.show()
        self.close()

    def create(self):
        global choose,player
        player='creator'
        choose=Choose('create')
        choose.show()
        self.report.setText('Waiting for opponent...')
        '''if player connected:
        global game
        game.show()'''
        self.close()

    def join(self):
        global player,game
        player='joiner'
        client.join()
        '''if game=='wordgame':
        game=WordGame()
        game.show()'''
        self.close()

'''
class Auth(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('auth.ui',self)
        self.finish.clicked.connect(self.auth)

    def auth(self):
        global player,choose
        player=self.input_nickname.text()
        self.close()
        choose=Choose()
        choose.show()
        self.close()
'''

class Choose(QWidget):
    def __init__(self,mode='AI'):
        super().__init__()
        uic.loadUi('choose.ui',self)
        self.mode=mode
        self.wordgame.clicked.connect(self.play_wg)

    def play_wg(self):
        global game
        game = WordGame()
        if self.mode=='create':
            client.create('wordgame')
        else:
            game.show()
        self.close()

'''
class SignIn(QWidget): # окно регистрации
    def __init__(self):
        super().__init__()
        uic.loadUi('signin.ui', self)
        self.signin.clicked.connect(self.login)

    def login(self):
        global player, game
        self.nickname = self.input_login.text()
        if not access(f'..\\Players\\{self.nickname}', F_OK):
            self.error.show()
            self.error.setText('Не знаю никого с таким ником...')
            return
        elif self.nickname == 'AI':
            self.error.show()
            self.error.setText('Эй, это же я! Самозванец несчастный!')
            return
        self.passwd = self.input_passwd.text()
        player = self.nickname
        with open(f'..\\Players\\{player}\\pwd', encoding='utf-8') as file:
            if self.passwd != ''.join(list(filter(lambda c: c.isalnum() or c == '_', list(file.read())))):
                self.error.show()
                self.error.setText('Неправильный пароль!')
                return
        game = WordGame()
        game.show()
        self.close()
'''

opponent='opponent'
player='player'
MAINDICT = Dictionary('..\\Database\\Russian\\words.txt') # основной словарь слов


class WordGame(QMainWindow): # главное окно игры
    def __init__(self):
        global MAINDICT, username
        super().__init__()
        uic.loadUi('main.ui', self)
        #self.log_AI = Log(AI)
        #self.log_player = Log(player)
        #self.pic_player1.setPixmap(QPixmap(f'..\\Players\\Gaknas\\userpic.jpg'))
        #clickable(self.pic_player1).connect(lambda: self.showstats(player))
        #self.nickname_player1.setText(player)
        #self.pic_player2.setPixmap(QPixmap(f'..\\Players\\{opponent}\\userpic.jpg'))
        #clickable(self.pic_player2).connect(lambda: self.showstats(AI))
        #self.nickname_player2.setText(AI)
        self.wlist = MAINDICT.data
        self.miss = 3
        self.word = self.wlist.pop(rnd(0, len(self.wlist)))
        if opponent=='AI':
            self.gameview.insertItem(0, f'{opponent}: {self.word}')
        elif player=='creator':
            pass
        elif player=='joiner':
            pass
        self.isrun = False
        self.help.triggered.connect(self.showhelp)
        #self.stats.triggered.connect(lambda: self.showstats(player))
        self.enter.clicked.connect(self.move)

    def move(self): # обработка хода
        global MAINDICT, player
        if not self.isrun:
            #self.log_AI.newgame()
            #self.log_AI.move(AI, str(self.word))
            #self.log_player.newgame()
            #self.log_player.move(AI, str(self.word))
            self.isrun = True
        playerword = Word(self.input.text().replace('ё', 'е'))
        self.input.clear()
        #self.log_AI.move(player, str(playerword))
        #self.log_player.move(player, str(playerword))
        self.gameview.insertItem(0, f'{player}: {playerword}')
        if not str(playerword):
            self.mistake('Эй, строка-то пустая! Повнимательнее, ладно? ;)')
            return
        '''if playerword not in MAINDICT and player == 'H1K0':
            ntf = NotificationDialog('Новое слово!', 'Такого слова я пока еще не знаю! Папа, ты уверен, что хочешь научить меня ему?', self)
            ntf.okcanl.accepted.connect(lambda: MAINDICT.add(playerword))
            ntf.okcanl.rejected.connect(lambda: self.mistake('Ну тогда я зачту тебе это как ошибку...'))
            ntf.exec()'''
        if playerword not in MAINDICT and player != 'H1K0':
            self.mistake('Я не знаю этого слова, а научить меня может только мой папа! :) Если хочешь добавить слово в базу, обратись к нему!')
            return
        elif playerword in MAINDICT and playerword not in self.wlist:
            self.mistake('Ты ввел уже использованное слово!')
            return
        elif not self.word >> playerword:
            self.mistake('Слово, конечно, замечательное, только сейчас оно немножко не к месту...')
            return
        if playerword in self.wlist:
            self.wlist.remove(playerword)
        available = list(filter(lambda w: playerword >> w, self.wlist))
        if available:
            self.word = available[rnd(0, len(available) - 1)]
            self.wlist.remove(self.word)
            #self.log_AI.move(AI, str(self.word))
            #self.log_player.move(AI, str(self.word))
            self.gameview.insertItem(0, f'{opponent}: {self.word}')
        else:
            self.win()
        del available

    def mistake(self, text): # обработка ошибки
        self.miss -= 1
        #self.log_AI.mistake(0, False)
        #self.log_player.mistake(3 - self.miss)
        if self.miss > 0:
            ntf = NotificationDialog('ОШИБКА!!!', text + f'\n\nТы сделал {3 - self.miss} {["ошибку", "ошибки"][1 - int(self.miss == 2)]}.', self)
            ntf.show()
            self.gameview.insertItem(0, f'--- ОШИБКА {3 - self.miss} ---')
        else:
            self.lose(text)

    def win(self): # обработка победы юзера
        ntf = NotificationDialog('ПОБЕДА!!!', 'Поздравляю, ты выиграл! С тобой очень весело играть!', self)
        ntf.show()
        del ntf
        #self.log_AI.lose()
        #self.log_AI.save()
        #self.log_player.win()
        #self.log_player.save()
        self.restart()

    def lose(self, error=None): # обработка поражения юзера
        text = ''
        if error is not None:
            text = f'{error}\nИ это была твоя третья ошибка! '
        text += 'Яху-у, я выиграла!\nНе расстраивайся, поражение - это всегда полезный опыт!'
        ntf = NotificationDialog('ПРОИГРЫШ!!!', text, self)
        ntf.show()
        del ntf
        #self.log_AI.win()
        #self.log_AI.save()
        #self.log_player.lose()
        #self.log_player.save()
        self.restart()

    def restart(self): # перезапуск игры
        global MAINDICT
        self.wlist = MAINDICT.data
        self.miss = 3
        self.word = self.wlist.pop(rnd(0, len(self.wlist)))
        self.gameview.clear()
        self.gameview.insertItem(0, f'{opponent}: {self.word}')
        self.isrun = False

    def showhelp(self): # показать справку
        dlg = HelpDialog(self)
        dlg.show()
        del dlg

    '''def showstats(self, user): # показать статистику
        if user == player:
            #self.log_player.save()
            #self.log_player.reload()
        elif user == AI:
            #self.log_AI.save()
            #self.log_AI.reload()
        dlg = StatsDialog(self, user)
        dlg.show()
        del dlg'''

    def closeEvent(self, event):
        if self.isrun:
            self.lose()


class HelpDialog(QDialog): # окно справки
    def __init__(self, parent):
        global MAINDICT
        super().__init__(parent)
        uic.loadUi('help.ui', self)
        self.number_of_words.setDigitCount(len(str(len(MAINDICT))))
        self.number_of_words.display(len(MAINDICT))


"""class StatsDialog(QDialog): # окно статистики
    def __init__(self, parent, user):
        global AI, player
        super().__init__(parent)
        uic.loadUi('stats.ui', self)
        self.setWindowTitle(f'Статистика: {user}')
        if user == AI:
            log = parent.log_AI
        else:
            log = parent.log_player
        wins = log.data.split('\n').count('--- ВЫИГРЫШ ---')
        loses = log.data.split('\n').count('--- ПРОИГРЫШ ---')
        misses = len(list(filter(lambda line: line.startswith('--- ОШИБКА'),
                                 log.data.split('\n'))))
        self.out.setText(f'''<p><strong>Всего сыграно:</strong> {len(log)}.</p>
<p><strong>Выиграно:</strong> {wins}.</p>
<p><strong>Проиграно:</strong> {loses}.</p>
<p><strong>Всего ошибок:</strong> {misses}.</p>''')
        del log, wins, loses, misses"""


class NotificationDialog(QDialog): # окно уведомлений
    def __init__(self, title, notification, parent):
        super().__init__(parent)
        uic.loadUi('notification.ui', self)
        self.setWindowTitle(title)
        self.out.setText(notification)


if __name__ == '__main__':
    from sys import argv
    app = QApplication(argv)
    start=Start()
    start.show()
    exit(app.exec_())
