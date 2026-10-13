from test.test_main import client
from main import app
from fastapi import status
from router.auth import get_current_user
from database import SessionLocal
from models import Transactions, Users
from datetime import date


def override_get_current_user():
    return {
        'id': 1,
        'username': 'testuser'
    }


app.dependency_overrides[get_current_user] = override_get_current_user

db = SessionLocal()
user = db.query(Users).filter(Users.id == 1).first()
if user is None:
    db.add(Users(
        id=1,
        username='testuser',
        email='testuser@example.com',
        hashed_password='testpassword'
    ))
    db.commit()
db.close()


def test_get_transactions():
    response = client.get('/transactions')
    assert response.status_code == status.HTTP_200_OK


def test_get_specific_transaction():
    db = SessionLocal()
    db.query(Transactions).filter(Transactions.id == 99).delete()
    db.add(Transactions(
        id=99,
        title='Groceries',
        amount=250,
        type='expense',
        category='Food',
        date=date(2026, 10, 1),
        owner_id=1
    ))
    db.commit()
    db.close()

    response = client.get('/transactions/99')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['title'] == 'Groceries'

    missing = client.get('/transactions/9999')
    assert missing.status_code == status.HTTP_404_NOT_FOUND


def test_create_transaction():
    request_data = {
        'title': 'Salary',
        'amount': 5000,
        'type': 'income',
        'category': 'Job',
        'date': '2026-10-01'
    }
    response = client.post('/transactions', json=request_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['title'] == 'Salary'
    assert response.json()['owner_id'] == 1

    invalid = client.post('/transactions', json={
        'title': 'Bad',
        'amount': -10,
        'type': 'income',
        'category': 'Job',
        'date': '2026-10-01'
    })
    assert invalid.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_transaction():
    request_data = {
        'title': 'Weekly groceries',
        'amount': 300
    }
    response = client.put('/transactions/99', json=request_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['title'] == 'Weekly groceries'
    assert response.json()['amount'] == 300

    missing = client.put('/transactions/9999', json={'title': 'Missing'})
    assert missing.status_code == status.HTTP_404_NOT_FOUND


def test_delete_transaction():
    response = client.delete('/transactions/99')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'Transaction deleted successfully'}

    missing = client.delete('/transactions/9999')
    assert missing.status_code == status.HTTP_404_NOT_FOUND
