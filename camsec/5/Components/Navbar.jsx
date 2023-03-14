import React from "react";

import { Link } from "react-router-dom";
import "./Header.css";
import logo from "./Images/icon.jfif";
import { ImHome3 } from "react-icons/im";
import { GiCctvCamera } from "react-icons/gi";
import { IoIosAddCircle } from "react-icons/io";
import { BiSelection } from "react-icons/bi";
import { RiNotification2Fill } from "react-icons/ri";
import { VscGraph } from "react-icons/vsc";
import { AiOutlineLogout } from "react-icons/ai";
import { Avatar } from "@mui/material";

const Navbar = () => {
  return (
    <div className="nav_head s" >
      <div className="imgcontainer n1" >
        <Avatar style={{background:'white',color:'black',width:'10vh'
        ,height:'10vh'}} src={logo} alt="Logo" />
       </div>
         <b className="bha">Bharat Kushwaha</b>
          <hr width='100%' size={4} color='black'></hr>
          <p className="nav_list f3" >
           <ImHome3 className="ico f4" />
           <Link to="/home" className="f3">
            Home
          </Link> 
      </p>
      <p className="nav_list f5">
        <GiCctvCamera className="ico f4" />
         <Link to="/Camerasetting" className="f3">
          Camera Setting
        </Link> 
      </p>
      <p className="nav_list"style={{background:'white',marginTop:'30px',color:'black'}}>
        <IoIosAddCircle className="ico"style={{background:'',fontSize:'20px',color:'black'}} />
         <Link to="/AddUser" id="hm"style={{background:'white',color:'black'}}>
          Add User
        </Link> 
      </p>
      <p className="nav_list"style={{background:'white',marginTop:'30px',color:'black'}}>
        <BiSelection className="ico"style={{background:'',fontSize:'20px',color:'black'}} />
        <Link to="/Areaselection" id="hm"style={{background:'white',color:'black'}}>
        Area Selection
        </Link>
      </p>
      <p className="nav_list"style={{background:'white',marginTop:'30px',color:'black'}}>
        <RiNotification2Fill className="ico"style={{background:'',fontSize:'20px',color:'black'}} />
        <Link to="/Eventoccur" id="hm"style={{background:'white',color:'black'}}>
        Event Occurence
        </Link>    
      </p>
      <p className="nav_list"style={{background:'white',marginTop:'30px',color:'black'}}>
        <VscGraph className="ico" style={{background:'',fontSize:'20px',color:'black'}}/>
        Visulization
      </p>
      <p className="nav_list"style={{background:'white',marginTop:'30px',color:'black'}}>
        <AiOutlineLogout className="ico" style={{background:'',fontSize:'20px',color:'black'}}/>
        Logout
      </p>
    </div>
  );
};

export default Navbar;
