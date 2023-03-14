import React, { useState, useEffect } from 'react';
import { FaLock } from 'react-icons/fa';
import { FaUserAlt } from 'react-icons/fa';
// import { url } from '../../GlobalUrl';
// import AccountCircleIcon from '@mui/icons/AccountCircle';
// import LockIcon from '@mui/icons/Lock';
// import Icon from '@material-ui/core/Icon';
// import account_circle from '@mui/icons-material/account_circle';
import axios from 'axios';
// import { useHistory } from 'react-router-dom';
import Stack from '@mui/material/Stack';
import Snackbar from '@mui/material/Snackbar';
import MuiAlert from '@mui/material/Alert';
import { Grid } from '@material-ui/core';
import { History } from '@material-ui/icons';

const Alert = React.forwardRef(function Alert(props, ref) {
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});
export default function App() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  // var history = useHistory();
  // const [email, setEmail] = useState("")
  // const [password, setPassword] = useState("")
  const [emailError, setEmailError] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const [passBorderColor, setPassBorderColor] = useState('#f7f7fa');
  const [emailBorderColor, setEmailBorderColor] = useState('#f7f7fa');
  const [visible, setVisible] = useState(false);
  const [msg, setMsg] = useState('');
  const [verify, setVerify] = useState(false);

  const [modal, setModal] = useState(false);

  // const toggle = () => {
  //   setModal(!modal);
  //   if (msg === 'Login Successful!') {
  //     window.location.replace('/home');
  //   }
  // };

  // async function verificationEmailApi() {
  //   setVerify(false);

  //   await axios
  //     .post(`${url}/api/email/verification/refresh/`, { email: email })
  //     .then((res) => {
  //       //console.log(res);
  //       setMsg(res.data.message);
  //       setVerify(false);
  //     })
  //     .catch((error) => {
  //       console.log(error);
  //       setVerify(false);
  //     });
  // }

  async function callApi() {
    // console.log("DATA", email, password);
    axios.defaults.headers.common['Authorization'] = ``;
    await axios
      .post('http://127.0.0.1:5000' + '/api/login', { email, password })
      .then((res) => {
        localStorage.setItem('login', res.data.access);
        localStorage.setItem('refresh_login', res.data.refresh);
        const login = localStorage.getItem('login');
        axios.defaults.headers.common['Authorization'] = `Bearer ${login}`;

        if (res.status == 203) {
          // alert("Please verify your email!");
          setMsg('Please verify your email!');
          setModal(true);
          setVerify(true);
        }

        if (res.status === 200) {
          setMsg('Login Successful!');
          window.location.replace('/home');
          // setModal(true)
          // alert("Login Successful!");
        }
      })
      .catch((error) => {
        // console.log(error.response);
        console.log(error);
        if (error && error.response && error.response.status === 401) {
          // alert(error.response.data.detail);
          setMsg('Invalid email or password');
          localStorage.setItem('token', null);
          axios.defaults.headers.common['Authorization'] = ``;
          setModal(true);
        }
      });
  }

  // const show_password = () => {
  //   setVisible(!visible);
  //   // if(e.target.checked){
  //   //     setVisible(true);
  //   // }
  //   // else{
  //   //   setVisible(false);

  //   // }
  // };

  // const handleEmail = (e) => {
  //   // console.log(e.target.value);
  //   setEmail(e.target.value);

  //   var emailRegex = '^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+[.]+[a-zA-Z]+$';

  //   const check = (mailID) => {
  //     if (mailID.match(emailRegex)) {
  //       return true;
  //     } else {
  //       return false;
  //     }
  //   };

  //   if (e.target.value.length === 0) {
  //     setEmailError('*Enter email address');
  //     setEmailBorderColor('1px solid red');
  //   } else if (!check(e.target.value)) {
  //     setEmailError('Not a valid email address');
  //     setEmailBorderColor('1px solid red');
  //   } else {
  //     setEmailError('');
  //     setEmailBorderColor('#f7f7fa');
  //   }
  // };

  // const handlePassword = (e) => {
  //   // console.log(e.target.value);
  //   setPassword(e.target.value);
  //   // console.log("LEN", e.target.value.length);

  //   if (e.target.value.length === 0) {
  //     setPasswordError('*Enter Password');
  //     setPassBorderColor('1px solid red');
  //   } else {
  //     setPasswordError('');
  //     setPassBorderColor('#f7f7fa');
  //   }
  // };

  // console.log("URL", url);


  const handleClick = () => {
    // e.preventDefault();
    console.log('tytytyt', email, password);
    if (email === '' || password === '') {
      setMsg('');
      setMsg('Please fill all the details');
      setModal(true);
      setVerify(false);
    } else {
      callApi();
    }
  };
  // const handleClick=async()=>{
  //   try {
  //     const response = await axios.post('http://127.0.0.1:5000/api/login', {email, password});
  //     console.log(response.data);
  //     // Display success message to user
  //     history.push('/home');
  //   } catch (error) {
  //     console.error(error);
  //     // Display error message to user
  //   }
  // }


  return (
    <div className="lpage">
      <div className="details">
        <div className="" style={{ marginLeft: '55vw' }}>
          <div class="container">
            <div className="logo" style={{ marginLeft: '213px' }}></div>
            {/* <form action=""> */}
            <div class="form-item" style={{ width: '236px', height: '40px' }}>
              <span
                class="material-icons-outlined"
                style={{
                  background: '#000000',
                  width: '0px',
                  borderRadius: '99px',
                  marginRight: '16px',
                }}
              >
                <FaUserAlt />
              </span>
              <input
                type="text"
                name="user"
                id="user"
                onChange={(e) => setEmail(e.target.value)}
                // placeholder="Email or Username"
              />
            </div>
            <div
              class="form-item"
              style={{ marginTop: '14px', height: '40px', width: '234px' }}
            >
              <span
                style={{
                  background: '#000000',
                  width: '0px',
                  marginRight: '16px',
                }}
                class="material-icons-outlined"
              >
                <FaLock style={{ background: '#000000' }} />
              </span>
              <input
                type="password"
                name="pass"
                onChange={(e) => setPassword(e.target.value)}
                id="pass"
                // placeholder="password"
              />
            </div>
            <button
              style={{ marginTop: '30px' }}
              type="submit"
              onClick={handleClick}
            >
              LOGIN
            </button>
            <b
              style={{
                fontSize: '12px',
                marginLeft: '367px',
                width: '100px',
                color: 'white',
              }}
            >
              <u style={{ color: 'white' }}>Forgot Password</u>
            </b>
          </div>
        </div>
      </div>
      {/* <Stack spacing={2} sx={{ width: '200%' }}>
        <Snackbar 
        anchorOrigin={{ vertical, horizontal }}
        open={open}
        onClose={handleClose}
        key={vertical + horizontal}
      ><Alert severity="error">{message}</Alert></Snackbar>
      </Stack> */}
    </div>
  );
}