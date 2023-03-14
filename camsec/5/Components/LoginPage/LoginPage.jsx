import React,{useState,useEffect} from "react";
import { FaLock } from "react-icons/fa";
import { FaUserAlt } from "react-icons/fa";
// import AccountCircleIcon from '@mui/icons/AccountCircle';
// import LockIcon from '@mui/icons/Lock';
// import Icon from '@material-ui/core/Icon';
// import account_circle from '@mui/icons-material/account_circle';
import axios from "axios"
import {useHistory} from "react-router-dom"
import Stack from '@mui/material/Stack';
import Snackbar from '@mui/material/Snackbar';
import MuiAlert from '@mui/material/Alert';
import { Grid } from "@material-ui/core";
const Alert = React.forwardRef(function Alert(props, ref) {
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});
const LoginPage = () => {
  const [password,setPassword]=useState('')
  const [email,setEmail]=useState('')
  const [state, setState] = React.useState({
    open: false,
    open2:false,
    vertical: 'top',
    horizontal: 'right',
  });
  const [message,setMessage]=useState('')
  const { vertical, horizontal, open } = state;  
  const handleClose = () => {
    setState({ ...state, open: false });
  };
  var history=useHistory()
  useEffect(function () {
    console.log("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",localStorage.getItem("data"))
    if(localStorage.getItem('d')!=null)
    {
      console.log(localStorage.getItem('d'))
      if(localStorage.getItem('t')!=null)
      {
      console.log(localStorage.getItem('t'))
      var body={email:localStorage.getItem('d'),password:localStorage.getItem('t')}  
      axios
      .post("http://127.0.0.1:5000/selectuser",body)
      .then(response => {console.log("ggggggggggggggggggggggggggg",response.data)
      if(response.data!='Pls Enter Valid Emailid And Password!')
      {
        console.log("gggggggg",response.data)
        response.data.map(hg=>{
        localStorage.setItem("d",hg.email)
        localStorage.setItem("t",hg.password)  
        localStorage.setItem("data",hg.type)
        localStorage.setItem("name",hg.name)
        })
        localStorage.setItem("id",JSON.stringify(response.data))
        history.replace({pathname:"/home",data:response.data})
      }
      else
      {
      }
      })
      }
    }
  }, []);
  const handleClick=async()=>{
    var  err=false
    const regex = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
    if(!email || regex.test(email) === false){
    setMessage("Pls Enter Valid Email Id")
    setState({open:true,vertical: 'top',
    horizontal: 'right'})
    err=true
    }
  if(!password)
  {
    setMessage("Pls Enter Password")
    setState({open:true,vertical: 'top',
    horizontal: 'right'})
    err=true 
  }
    if(!err)
    {
      var body={email:email,password:password} 
      console.log(body)  
      axios
      .post("http://127.0.0.1:5000/selectuser",body)
      .then(response => {console.log(response)
      if(response.data!='Pls Enter Valid Emailid And Password!')
      {
        console.log("gggggggg",response.data)
        response.data.map(hg=>{
        localStorage.setItem("d",hg.email)
        localStorage.setItem("t",hg.password)  
        localStorage.setItem("data",hg.type)
        localStorage.setItem("name",hg.name)
        })
        localStorage.setItem("id",JSON.stringify(response.data))
        history.replace({pathname:"/home",data:response.data})
      }
      else
      {
        setMessage(response.data)
        setState({open:true,vertical: 'top',
        horizontal: 'right'})
      }
    })
  
  }
  
     }
  return (
    <div className="lpage">
      <div className="moto">
        <span id="lhead">CAMSEC.AI</span>
        <hr style={{ height: "3px" }} />
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Mitigate
        Manual Monitoring

        {/* <img src="camsec\src\camsec_name_tagline.png" alt="camsec tagline" /> */}
      </div>
      <div className="details">
        

        <div className="login">
          {/* old one */}
          {/* <form>
            
            
            <div class="form mb-4 transparent-input">
              <input
                type="email"
                id="typeEmail"
                class="form-control transparent-input"
              />
              <label class="form-label" for="typeEmail" id="logincolor">
                Email address
              </label>
            </div>

            
            <div class="form-outline mb-4">
              <input type="password" id="form2Example2" class="form-control" />
              <label class="form-label" for="form2Example2" id="logincolor">
                Password
              </label>
            </div>

            
            <button type="submit" class="btn btn-light btn-block mb-4">
              Sign in
            </button>
          </form> */}

          {/* new form */}

          {/* <!-- for form container --> */}
          <div class="container">
          <div className="logo"> 
        </div>
            {/* <form action=""> */}
              <div class="form-item">
                <span class="material-icons-outlined">
                  <FaUserAlt />
                </span>
                <input
                  type="text"
                  name="user"
                  id="user"
                  onChange={(e)=>setEmail(e.target.value)}
                  placeholder="Email or Username"
                />
              </div>

              <div class="form-item">
                <span class="material-icons-outlined">
                  <FaLock />
                </span>
                <input
                  type="password"
                  name="pass"
                  onChange={(e)=>setPassword(e.target.value)}
                  id="pass"
                  placeholder="password"
                />
              </div>

              <button type="submit" onClick={()=>handleClick()}>LOGIN</button>
            {/* </form> */}
          </div>
        </div>
      </div>
      <Stack spacing={2} sx={{ width: '200%' }}>
        <Snackbar 
        anchorOrigin={{ vertical, horizontal }}
        open={open}
        onClose={handleClose}
        key={vertical + horizontal}
      ><Alert severity="error">{message}</Alert></Snackbar>
      </Stack>
    </div>
  );
};

export default LoginPage;
