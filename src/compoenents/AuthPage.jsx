import axios from "axios";
import Cookies from "js-cookies";
import React, { useEffect } from "react";

const AuthPage = () => {
  const getData = () =>
    axios
      .get("http://127.0.0.1:8000/protected", {
        headers: {
          token: "testToken",
        },
      })
      .then((res) => console.log(res.data))
      .catch((err) => console.error(err));

  useEffect(() => getData(), []);

  return (
    <div>
      <h>Login here!</h>
    </div>
  );
};

export default AuthPage;
