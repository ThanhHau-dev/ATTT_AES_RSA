// tạo chức năng hiển thị cho form input
// Nhấn vào nút bắt đầu mã hóa, giải mã thì form input tắt
// form kết quả hiện ra

const btn_Start = document.querySelector(".btn_Start");
const btn_success = document.querySelector(".btn-success");
const formInput = document.querySelector(".Encryption");
const output = document.querySelector(".output");
const btn_End = document.querySelector(".btn_End");

const geturlApi = ""; // GET
const posturlApi = "http://localhost:8080/api/data"; // POST


btn_Start.addEventListener("click", () => {
  formInput.style.display = "none";
  output.style.display = "block";
  postApi();
});

btn_success.addEventListener("click", () => {
  formInput.style.display = "none";
  output.style.display = "block";
  postApi();
});

btn_End.addEventListener("click", () => {
  output.style.display = "none";
  formInput.style.display = "block";
});

// POST dữ liệu về cho backend xử lý, đã rest với fake api thành công
// lúc nào BE xong thì mở
/*
function postApi() {
  // Dữ liệu từ ô input
  var inputData = document.querySelector("#inputData").value;
  var inputKey = document.querySelector("#inputKey").value;

  // object chứa dữ liệu từ người dùng
  var dataUser = {
    data: inputData,
    key: inputKey,
  };
  // console.log(dataUser);

  fetch(geturlApi, {
    method: "POST",
    headers: {
      "Content-Type": "application/json", // định dạng cho json á
    },
    body: JSON.stringify(dataUser), // chuyển đổi cái object sang json
  })
    .then((sucsess) => {
      console.log("Đã gửi dữ liệu đi thành công: " + sucsess);
      return sucsess.json()
    })
    .then((done)=> {
       //callAPIkq();  // đợi post xong đã, server xử lý có kết quả thì callAPi mới gọi,
        // khi nào hoàn thiện BE thì mới mở cái này, h đang test fake api

        console.log(done);
    })
    .catch((error) => {
      console.log("Đã xảy ra lỗi khi gửi đi dữ liệu: " + error);
    })
    .finally(() => {
      console.log("Hoàn thành quá trình POST");
    });
};
*/


// callapi cho bảng kết quả
function callAPIkq() {
  fetch(geturlApi)
    .then((datajson) => datajson.json())
    .then((datajs) => {
      let htmlkq = datajs.map((dataRender) => {
        return `
                    <h2>${dataRender.kq1}</h2>
                `;
      });

      document.querySelector("#dataRender").innerHTML = htmlkq;
    })
    .catch((error) => {
      console.log("Đã xảy ra lỗi trong quá trình callApi: " + error);
    })
    .finally((done) => {
      console.log("Hoàn thành quá trình callApi.");
    });
};
callAPIkq();



// sương sương xong FE, cần coi kĩ lại chỗ callapi chờ post