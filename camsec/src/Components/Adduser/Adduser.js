import React, { useState } from "react";
import Username from "./Username";
import Userid from "./Userid";
import axios from "axios";
import {AiOutlineDownload,IoCloudDone,MdOutlineDelete,MdMessage,AiOutlineCloudDownload,BsCloudArrowUp} from "react-icons/all"
import Authority from "../Camsetting/Authority/Authority1";
import { MDBCard, MDBCardBody, MDBCardTitle } from "mdb-react-ui-kit";
import "./AddUser.css"
const Adduser = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [mobileno, setMobileno] = useState('');
  const [company, setCompany] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
const [f2,setF2]=useState(false)
const [image, setImage] = useState({
  bytes: "",
  file: "/noimage.jpg",
});
const [i1,setI1]=useState(false)
const [f1,setF1]=useState(false)
const handle=(event)=>{
  setImage({
      bytes: event.target.files[0],
      file: URL.createObjectURL(event.target.files[0]),
       })
      setF1(true)
}
const handlesubmit=()=>{
  const data = {
    name: name,
    email: email,
    mobileno: mobileno,
    company: company,
    password: password
  };
  axios.post('/register', data)
      .then(response => {
        setMessage("User registration successful");
      })
      .catch(error => {
        setMessage(error.response.data.message);
      });
  // console.log(data);
}
const handle77=()=>{
  setF2(false)
  setI1(true)
}
const handle1=()=>{
    setImage({
      bytes: "",
      file: "/noimage.jpg",
    })
    setF1(false)
}
  return (
    <>
    {f2===false?
    <div className="adduser">
      <div className="home">
        <div className="head">
          <div className="heading">
            <div className="head1">HEALTHCARE SEC</div>
            <div className="head2">CAMSEC.AI</div>
          </div>
        </div>
        </div>
        <hr id="hr"/>
           <div className="adduser-panel2">
            <div className="adduser-fields">
                <div className="username">
                <div className="cam-selc-card" style={{marginLeft:'5px'}}>
                <MDBCard className="cam-selc-card">
                 <MDBCardBody>
                 <MDBCardTitle  className="name">Name</MDBCardTitle>
                  <form >
                  <label>
                  <input className="te" type="text" value={name} onChange={e => setName(e.target.value)}/>
                  </label>
                 </form>
                 </MDBCardBody>
                </MDBCard>
                </div>
                </div>
                <div className="userid">
                <div className="cam-selc-card">
                 <MDBCard className="cam-selc-card">
                  <MDBCardBody>
                  <MDBCardTitle className="name">Password</MDBCardTitle>
                  <form >
                   <label>
                  <input className="te" type="user id" value={password} onChange={e => setPassword(e.target.value)}/>
                </label>
                </form>
              </MDBCardBody>
            </MDBCard>
           </div>
          </div>
          <div className="userid">
                <div className="cam-selc-card">
                 <MDBCard className="cam-selc-card">
                  <MDBCardBody>
                  <MDBCardTitle className="name">Email</MDBCardTitle>
                  <form >
                   <label>
                  <input className="te" type="user id" value={email} onChange={e => setEmail(e.target.value)} />
                </label>
                </form>
              </MDBCardBody>
            </MDBCard>
           </div>
          </div>
          <div className="userid">
                <div className="cam-selc-card">
                 <MDBCard className="cam-selc-card">
                  <MDBCardBody>
                  <MDBCardTitle className="name">Mobile No.</MDBCardTitle>
                  <form >
                   <label>
                  <input className="te" type="user id" value={mobileno} onChange={e => setMobileno(e.target.value)} />
                </label>
                </form>
              </MDBCardBody>
            </MDBCard>
           </div>
          </div>
          <div className="userid">
                <div className="cam-selc-card">
                 <MDBCard className="cam-selc-card">
                  <MDBCardBody>
                  <MDBCardTitle className="name">Company</MDBCardTitle>
                  <form >
                   <label>
                  <input className="te" type="user id" value={company} onChange={e => setCompany(e.target.value)} />
                </label>
                </form>
              </MDBCardBody>
            </MDBCard>
           </div>
          </div>
          {/* <div className="userauthority">
          <Authority  />
          </div> */}
          </div>
          <div className="adduser-buttons">
          {i1===false?
          <button onClick={()=>setF2(true)} className='bu1'>
            <AiOutlineDownload
             style={{marginRight:'10px'}} />Upload Image</button>  
             :<div className="r">
             <img style={{height:'8vh',width:'8vh'}} src={image.file}></img>
              <button className="bu2"><IoCloudDone className="ic" />Uploaded</button>
              </div>}
                <button onClick={()=>handlesubmit()}className='bu5'><MdMessage 
                  style={{marginRight:'10px'}} />Register</button>
                  </div>
                </div>    
            </div>
    :
    <div className="adduser">
    <div className="home">
      <div className="head">
        <div className="heading">
          <div className="head1">HEALTHCARE SEC</div>
          <div className="head2">CAMSEC.AI</div>
        </div>
      </div>
      </div>
      <hr id="hr"/>
      <div className="adduser-panel1">
          <div className="adduser-fields1">
              {f1===false?<div>
              <div>
               <div>
                <h2 className="up"><b>Upload Your Image</b></h2>
                <b className="p">PNG AND JPG files are allowed</b>
                 <div className="up1">
                 <BsCloudArrowUp className="bs"/>
                  </div>
                  <div className="up2">
                 <div>
                <input onChange={(event) =>handle(event)
                } type="file" id="actual-btn" hidden />
                <label id="choose"className="t1"  for="actual-btn">Drag And drop or browes to choose a file</label>
                </div>
              </div>
              </div>
             </div>
            </div>:
           <div className="img1"><img className="img2"
            src={image.file}></img>
           </div>} 
           <div className="ce">
           <button onClick={()=>handle77()} className='on'><AiOutlineDownload
            style={{marginRight:'6px'}} />Save</button>
           <button onClick={()=>handle1()} className='on1'><MdOutlineDelete 
            style={{marginRight:'10px'}} />Discard</button>
          </div>
        </div> 
      </div>    
  </div>
    }</>
  );
};

export default Adduser;
