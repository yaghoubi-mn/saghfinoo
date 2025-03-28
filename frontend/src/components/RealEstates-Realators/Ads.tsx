import AdsCart from "../AdsCart";
import { Title } from "@/constant/Constants";
import { AdsDataType } from "@/types/Type";
import PaginationComponent from "../Pagination";
import Skeleton from "react-loading-skeleton";
import "react-loading-skeleton/dist/skeleton.css";
import Image from "next/image";
import { QueryObserverResult, RefetchOptions } from "@tanstack/react-query";
import MobileFilter from "../Filter/MobileFilter";
import { useState } from "react";
import DesktopFilter from "../Filter/desktop/DesktopFilter";

export type ProvinceType =
  | { name: string | undefined; id: number | undefined }
  | undefined;

type AdsType = {
  title: string;
  status: "error" | "success" | "pending";
  data: AdsDataType[] | undefined;
  totalPages: number | undefined;
  refetch: (options?: RefetchOptions) => Promise<
    QueryObserverResult<
      {
        data: AdsDataType[];
        totalPages: number;
      },
      Error
    >
  >;
  isFetching: boolean;
};
export default function Ads({
  title,
  status,
  data,
  totalPages,
  refetch,
  isFetching,
}: AdsType) {
  const [isOpenFilterMobileModal, setIsOpenFilterMobileModal] =
    useState<boolean>(false);

  return (
    <div className="mt-10 flex flex-col p-4 md:mt-14 md:p-8">
      {status === "pending" ? (
        <Skeleton
          width={150}
          height={25}
          className="md:!w-[300px] md:!h-[30px]"
        />
      ) : (
        <>
          <Title title={title} />

          <div className="w-full mt-5">
            <MobileFilter
              isOpen={isOpenFilterMobileModal}
              setIsOpen={setIsOpenFilterMobileModal}
              isViewMore={false}
            />
            <DesktopFilter isViewMore={false} />
          </div>
        </>
      )}

      <AdsCart
        data={data}
        isloading={status === "pending"}
        refetch={refetch}
        isFetching={isFetching}
      />

      {status === "success" && data && data?.length <= 0 && (
        <div className="flex flex-col items-center mt-5 w-full">
          <Image
            width={130}
            height={130}
            className="md:w-52 md:h-52 lg:w-56 lg:h-56"
            src="/icons/NoDataPage.svg"
            alt="NO Data"
          />
          <p className="text-sm md:text-base lg:text-lg">
            متاسفانه آگهی برای نمایش یافت نشد ):
          </p>
        </div>
      )}

      <PaginationComponent totalPages={totalPages} />
    </div>
  );
}
