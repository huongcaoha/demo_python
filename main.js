
        let a = Number(prompt("hay nhap so a"));
        let b = Number(prompt("hay nhap so b"));
        let c = prompt(`hay chon mot trong cac phep tinh sau:
        1. phep cong
        2.phep tru
        3.phep nhan
        4.phep chia`);
      
        switch(parseInt(c)){
            case 1:
                alert(`kết quả của a + b = ${parseInt(a) + parseInt(b)}`);
                break;
            case 2:
                alert(`kết quả của a - b = ${parseInt(a) - parseInt(b)}`);
                break;
            case 3:
                alert(`kết quả của a x b = ${parseInt(a) * parseInt(b)}`);
                break;
            case 4:
                alert(`kết quả của a : b = ${parseInt(a) / parseInt(b)}`);
                break;
        }