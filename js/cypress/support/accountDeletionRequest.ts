interface AccountVO {
  accountId: number;
}

interface AccountDeletionRequestVO {
  RequestVO: {
    csrf: string;
    data: {
      AccountVO: AccountVO;
    }[];
  };
}

function isAccountVO(obj: unknown): obj is AccountVO {
  return (
    typeof obj === "object" &&
    !!obj &&
    "accountId" in obj &&
    typeof obj.accountId === "number"
  );
}

export class AccountDeletionRequest {
  private account: AccountVO = { accountId: 0 };

  private csrf = "";

  public constructor() {
    this.setCurrentAccountVO();
    this.setCsrf();
  }

  public getRequestVO(): AccountDeletionRequestVO {
    return {
      RequestVO: {
        csrf: this.csrf,
        data: [
          {
            AccountVO: this.account,
          },
        ],
      },
    };
  }

  private setCurrentAccountVO(): void {
    const localstorageAccount = localStorage.getItem("account");
    if (localstorageAccount === null || localstorageAccount.length === 0) {
      throw new Error("Account not defined in localStorage");
    }
    const createdAccount: unknown = JSON.parse(localstorageAccount);
    if (isAccountVO(createdAccount)) {
      this.account = { accountId: createdAccount.accountId };
    }
  }

  private setCsrf(): void {
    const localstorageCsrf: unknown = JSON.parse(
      sessionStorage.getItem("CSRF") ?? `""`,
    );
    if (typeof localstorageCsrf !== "string") {
      throw new Error("sessionStorage csrf type not a string");
    }
    this.csrf = localstorageCsrf;
  }
}
