import CustomButton from "@/components/CustomButton";
import Image from "next/image";
import { useRouter } from "next-nprogress-bar";

export default function Error() {
  const router = useRouter();

  return (
    <>
      <p className="md:text-xl lg:text-2xl font-bold">
        مشکلی در ثبت آگهی شما به وجود آمده !
      </p>

      <p className="text-[#717171] text-sm md:text-base lg:text-xl mt-4 text-center">
        در قسمت ثبت آگهی، خطای مربوط به اطلاعات
        <br />
        برای شما مشخص شده است.
      </p>

      <CustomButton
        radius="sm"
        variant="bordered"
        className="text-primary border-primary border mt-6"
        onPress={() => router.push("/adPosting")}
      >
        برگشت به ثبت آگهی
      </CustomButton>

      <i className="mt-8 md:mt-5">
        <Image
          width={180}
          height={180}
          src="/icons/Folder.svg"
          alt="Error"
          className="md:w-[300px] md:h-[300px]"
        />
      </i>
    </>
  );
}