#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
User Manager для синхронизации пользователей Telegram бота с CSV
Версия: 1.0
"""

import csv
import fcntl
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict

CSV_FILE = '/var/www/bigdaddy_ff/user.csv'

class UserManager:
    """Управление пользователями в CSV файле"""
    
    @staticmethod
    def save_user(
        telegram_id: int,
        name: str = '',
        phone: str = '',
        dob: str = '',
        addr: str = '',
        username: str = ''
    ) -> bool:
        """
        Сохранение или обновление пользователя в CSV
        
        Args:
            telegram_id: ID пользователя в Telegram (обязательно)
            name: ФИО пользователя
            phone: Номер телефона
            dob: Дата рождения (формат: YYYY-MM-DD)
            addr: Адрес доставки
            username: Username в Telegram (с @ или без)
        
        Returns:
            bool: True если успешно, False если ошибка
        
        Example:
            >>> UserManager.save_user(
            ...     telegram_id=123456789,
            ...     name='Иван Иванов',
            ...     phone='79991234567',
            ...     dob='1990-01-15',
            ...     addr='Москва, ул. Ленина, д. 1',
            ...     username='@ivan'
            ... )
            True
        """
        try:
            telegram_id_str = str(telegram_id)
            
            # Нормализуем username
            if username and not username.startswith('@'):
                username = f'@{username}'
            
            # Создаём файл если не существует
            if not Path(CSV_FILE).exists():
                Path(CSV_FILE).parent.mkdir(parents=True, exist_ok=True)
                with open(CSV_FILE, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(
                        f, 
                        fieldnames=['telegram_id', 'name', 'phone', 'dob', 'addr', 'username']
                    )
                    writer.writeheader()
                print(f"📝 Создан новый CSV файл: {CSV_FILE}")
            
            # Читаем существующие данные
            rows = []
            with open(CSV_FILE, 'r', encoding='utf-8') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_SH)  # Shared lock для чтения
                reader = csv.DictReader(f)
                rows = list(reader)
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            
            # Ищем пользователя
            user_found = False
            for i, row in enumerate(rows):
                if row.get('telegram_id') == telegram_id_str:
                    # Обновляем данные (сохраняем старые если новые пустые)
                    rows[i] = {
                        'telegram_id': telegram_id_str,
                        'name': name or row.get('name', ''),
                        'phone': phone or row.get('phone', ''),
                        'dob': dob or row.get('dob', ''),
                        'addr': addr or row.get('addr', ''),
                        'username': username or row.get('username', '')
                    }
                    user_found = True
                    print(f"✅ Обновлен пользователь: {telegram_id} ({name or 'без имени'})")
                    break
            
            # Если не найден - добавляем нового
            if not user_found:
                rows.append({
                    'telegram_id': telegram_id_str,
                    'name': name,
                    'phone': phone,
                    'dob': dob,
                    'addr': addr,
                    'username': username
                })
                print(f"➕ Добавлен новый пользователь: {telegram_id} ({name or 'без имени'})")
            
            # Записываем обратно
            with open(CSV_FILE, 'w', encoding='utf-8', newline='') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)  # Exclusive lock для записи
                
                fieldnames = ['telegram_id', 'name', 'phone', 'dob', 'addr', 'username']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
                
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            
            return True
            
        except Exception as e:
            print(f"❌ Ошибка сохранения пользователя {telegram_id}: {e}")
            return False
    
    @staticmethod
    def get_user(telegram_id: int) -> Optional[Dict[str, str]]:
        """
        Получить данные пользователя из CSV
        
        Args:
            telegram_id: ID пользователя в Telegram
        
        Returns:
            dict: Данные пользователя или None если не найден
        
        Example:
            >>> user = UserManager.get_user(123456789)
            >>> print(user['name'])
            'Иван Иванов'
        """
        try:
            if not Path(CSV_FILE).exists():
                print(f"⚠️ CSV файл не найден: {CSV_FILE}")
                return None
            
            telegram_id_str = str(telegram_id)
            
            with open(CSV_FILE, 'r', encoding='utf-8') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_SH)  # Shared lock
                reader = csv.DictReader(f)
                
                for row in reader:
                    if row.get('telegram_id') == telegram_id_str:
                        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                        return row
                
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            
            print(f"ℹ️ Пользователь {telegram_id} не найден в CSV")
            return None
            
        except Exception as e:
            print(f"❌ Ошибка чтения данных пользователя {telegram_id}: {e}")
            return None
    
    @staticmethod
    def delete_user(telegram_id: int) -> bool:
        """
        Удалить пользователя из CSV
        
        Args:
            telegram_id: ID пользователя в Telegram
        
        Returns:
            bool: True если удален, False если не найден или ошибка
        """
        try:
            if not Path(CSV_FILE).exists():
                return False
            
            telegram_id_str = str(telegram_id)
            
            # Читаем данные
            rows = []
            with open(CSV_FILE, 'r', encoding='utf-8') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_SH)
                reader = csv.DictReader(f)
                rows = [row for row in reader if row.get('telegram_id') != telegram_id_str]
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            
            # Записываем обратно
            with open(CSV_FILE, 'w', encoding='utf-8', newline='') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                
                fieldnames = ['telegram_id', 'name', 'phone', 'dob', 'addr', 'username']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
                
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            
            print(f"🗑️ Удален пользователь: {telegram_id}")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка удаления пользователя {telegram_id}: {e}")
            return False
    
    @staticmethod
    def get_all_users() -> list:
        """
        Получить всех пользователей из CSV
        
        Returns:
            list: Список всех пользователей
        """
        try:
            if not Path(CSV_FILE).exists():
                return []
            
            users = []
            with open(CSV_FILE, 'r', encoding='utf-8') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_SH)
                reader = csv.DictReader(f)
                users = list(reader)
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            
            return users
            
        except Exception as e:
            print(f"❌ Ошибка чтения всех пользователей: {e}")
            return []
    
    @staticmethod
    def count_users() -> int:
        """Подсчет количества пользователей"""
        return len(UserManager.get_all_users())


# Тестирование модуля
if __name__ == '__main__':
    print("═══════════════════════════════════════")
    print("  Тестирование UserManager")
    print("═══════════════════════════════════════")
    print()
    
    # Тест 1: Создание пользователя
    print("Тест 1: Создание пользователя...")
    result = UserManager.save_user(
        telegram_id=123456789,
        name='Тест Тестов',
        phone='79991234567',
        dob='1990-01-01',
        addr='Тестовый адрес',
        username='@test'
    )
    
    if result:
        print("✅ Пользователь создан")
    else:
        print("❌ Ошибка создания")
    
    print()
    
    # Тест 2: Чтение пользователя
    print("Тест 2: Чтение пользователя...")
    user = UserManager.get_user(123456789)
    
    if user:
        print(f"✅ Пользователь найден:")
        print(f"   Имя: {user.get('name')}")
        print(f"   Телефон: {user.get('phone')}")
        print(f"   Адрес: {user.get('addr')}")
    else:
        print("❌ Пользователь не найден")
    
    print()
    
    # Тест 3: Обновление пользователя
    print("Тест 3: Обновление пользователя...")
    result = UserManager.save_user(
        telegram_id=123456789,
        phone='79999999999',  # Новый телефон
        addr='Новый адрес'     # Новый адрес
    )
    
    if result:
        print("✅ Данные обновлены")
        user = UserManager.get_user(123456789)
        print(f"   Новый телефон: {user.get('phone')}")
        print(f"   Новый адрес: {user.get('addr')}")
    else:
        print("❌ Ошибка обновления")
    
    print()
    
    # Тест 4: Подсчет пользователей
    print("Тест 4: Подсчет пользователей...")
    count = UserManager.count_users()
    print(f"✅ Всего пользователей: {count}")
    
    print()
    
    # Тест 5: Удаление пользователя
    print("Тест 5: Удаление тестового пользователя...")
    result = UserManager.delete_user(123456789)
    
    if result:
        print("✅ Пользователь удален")
    else:
        print("❌ Ошибка удаления")
    
    print()
    print("═══════════════════════════════════════")
    print("  Все тесты завершены!")
    print("═══════════════════════════════════════")
    
    # Показываем содержимое CSV
    print()
    print("Содержимое user.csv:")
    print("-" * 60)
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            print(f.read())
    except:
        print("Файл не найден или ошибка чтения")

