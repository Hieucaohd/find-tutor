# cài đặt findTutor

## Cách 1:

- cài python.
- cài pip.
- đối với windown thì nhớ đưa python và pip vào biến môi trường toàn cục.
- Mỗi lần pull về thì nhập các lệnh sau:
- mở terminal trong folder findTutor:
  - gõ câu lệnh: pip install -r requirements.txt
- mở terminal trong folder findTutor: 
  - gõ câu lệnh: python manage.py runserver

## Cách 2:
- cài python
- cài pip 
- đối với windown thì nhớ đưa python và pip vào biến môi trường toàn cục.
- tạo một môi trường ảo, nhập lệnh: python -m venv [tên thư mục chứa môi trường ảo] (giả sử là DjangoEnv)
- Mỗi lần pull về thì nhập lần lượt các lệnh sau: 
- Đầu tiên cd tới thư mục chứa môi trường ảo (cd DjangoEnv), nhập lệnh: source bin/active
- Sau đó lại cd tới thư mục chứa project vừa pull về (cd findTutor), nhập lệnh: pip install -r requirements.txt
- Để chạy server, nhập lệnh: python manage.py runserver.

# đọc biểu đồ graphQL:

## link diagram: https://drive.google.com/file/d/1X963zE-qAiYTSULvq8bAS9IiedaGeXnF/view?usp=sharing

## Sự liên quan giữa các bảng:
- các bảng được liên kết với nhau bằng các đường thẳng có mũi tên:
  - mũi tên một chiều: quan hệ one-to-many. Vd: một parent sẽ có nhiều paren-room
  - mũi tên 2 chiều: quan hệ one-to-one. Vd: mỗi user chỉ có một parent
- link test: 
  - Graphiql: http://tim-gia-su.herokuapp.com/findTutor/graphql (nhấn ctrl+space để xem các gợi ý)
  - Hoặc postman.


