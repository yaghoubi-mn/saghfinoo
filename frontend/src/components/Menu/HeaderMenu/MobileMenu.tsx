"use client";
import Image from "next/image";
import { useState } from "react";
import { Button } from "@nextui-org/button";
import { navigationMenuType } from "@/types/Type";
import { useModalStore, useUserInfo } from "@/store/Register";
import { useEffect } from "react";

type mobileMenuType = {
  NavigationMenu: navigationMenuType;
};

export default function MobileMenu({ NavigationMenu }: mobileMenuType) {
  const [openMenu, setOpenMenu] = useState<boolean>();
  const { setOpen } = useModalStore();
  const { userInfo } = useUserInfo();
  const [isLogin, setIsLogin] = useState<boolean>();

  useEffect(() => {
    console.log(userInfo);
    
    if (userInfo !== undefined) {
      setIsLogin(true);
    } else {
      setIsLogin(false);
    }
  }, [userInfo]);

  const ClickRegister = () => {
    if (!isLogin) {
      setOpen(true);
    }
  };

  return (
    <>
      <nav
        className="flex w-full z-40 bg-white p-3 top-0 justify-between shadow
       items-center fixed md:hidden"
      >
        <Button
          isIconOnly
          size="sm"
          radius="full"
          variant="light"
          onPress={() => setOpenMenu(true)}
        >
          <Image width={24} height={24} src="icons/menu.svg" alt="" />
        </Button>
        <Image width={72} height={32} src="/icons/Logo.svg" alt="" />
        <Button
          size="sm"
          variant="light"
          className="p-1 px-2 border border-red-600 text-[12px] font-medium
           rounded-[8px] text-red-600"
        >
          ثبت آگهی
        </Button>
      </nav>

      <div
        className={`absolute w-full h-screen bg-white hidden z-50 top-0 ${
          openMenu ? "openMenu" : "closeMenu"
        }`}
      >
        <div className="w-full flex flex-col py-5">
          <div className="w-full flex justify-end px-3">
            <Button
              isIconOnly
              size="sm"
              variant="light"
              onPress={() => setOpenMenu(false)}
            >
              <Image
                width={24}
                height={24}
                src="/icons/close-circle.svg"
                alt=""
              />
            </Button>
          </div>

          <div
            onClick={ClickRegister}
            className="w-full bg-gray-100 px-2 py-5 mt-4 flex items-center"
          >
            <Image
              width={isLogin ? 30 : 20}
              height={isLogin ? 30 : 20}
              src="/icons/profile-circle.svg"
              alt=""
            />{" "}
            {isLogin && (
              <Image
                width={20}
                height={20}
                className="mr-2"
                src="/icons/edit.svg"
                alt=""
              />
            )}
            <p className="mr-2 text-xs">
              {isLogin
                ? `${userInfo?.first_name} ${userInfo?.last_name}`
                : "ورود یا ثبت نام"}
            </p>
            {isLogin && (
              <Image
                width={20}
                height={20}
                src="/icons/arrow-left-2.svg"
                className="mr-2"
                alt=""
              />
            )}
          </div>
          <div className="mt-5 flex items-center justify-between px-2">
            <div className="flex items-center">
              <Image
                width={20}
                height={20}
                src="/icons/add-circle.svg"
                alt=""
              />
              <p className="text-xs mr-2">ثبت آگهی</p>
            </div>
            <Image width={20} height={20} src="/icons/arrow-left.svg" alt="" />
          </div>

          {NavigationMenu.map((item, index) => {
            return (
              <div
                key={index}
                className="mt-7 flex items-center justify-between px-2"
              >
                <div className="flex items-center">
                  <Image width={20} height={20} src="/icons/house.svg" alt="" />
                  <p className="text-xs mr-2">{item.title}</p>
                </div>
                <Image width={20} height={20} src={item.icon} alt="" />
              </div>
            );
          })}
        </div>
      </div>
    </>
  );
}
